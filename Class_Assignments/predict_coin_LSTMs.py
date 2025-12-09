"""Author: Zanyar Zohourian Shahzadi
Date: 2025-07-19
License: CC BY-NC-SA 4.0
Description:
"""

import numpy as np
import pandas as pd
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from coin_data import depth_chart_live, get_coin_price
from tensorflow.keras.callbacks import EarlyStopping


def create_model(mode='1', coin='btc', model='MLP', in_seq_len='1', out_seq_len='1'):
    global mae

    if mode == '1':
        df = pd.read_csv(f'{coin}_order_book_summary.csv')
        X = df[['Mean Bids Price', 'Mean Asks Price']].values
        # X = df[['Mean Bids Price', 'Mean Bids Size', 'Mean Asks Price', 'Mean Asks Size']].values
        Y = df['Price After 1min'].values
    else:
        create_xminute_data(mode, coin)
        df = pd.read_csv(f'{coin}_order_book_{mode}min_summary.csv')
        X = df[['Mean Bids Price', 'Mean Asks Price']].values
        # X = df[['Mean Bids Price', 'Mean Bids Size', 'Mean Asks Price', 'Mean Asks Size']].values
        Y = df[f'Price After {mode}min'].values

    modelName = model.upper()

    if model == 'MLP':
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.1, shuffle=True
        )

        model = keras.Sequential([
            layers.Input(shape=(X_train.shape[1],)),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(1)
        ])

    elif model == 'LSTM':
        x, y = [], []
        in_seq_len = int(in_seq_len)
        out_seq_len = int(out_seq_len)

        for i in range(len(X) - in_seq_len - out_seq_len + 1):
            x.append(X[i: i + in_seq_len])
            y.append(Y[i + in_seq_len: i + in_seq_len + out_seq_len])

        x, y = np.array(x), np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(
            x, y, test_size=0.1, shuffle=False
        )

        modelVar = input(
            "\nWhat type of LSTM model do you want to create? choose a number:\n"
            "1: LSTM: Fixed input and output sequence lengths that can be different.\n"
            "2: Stacked LSTM: Same as LSTM with stacked LSTM layers.\n"
        ).strip().lower() or 'varin-fixedout'

        match modelVar:
            case '1':
                model = keras.Sequential([
                    layers.Input(shape=(None, X_train.shape[2])),
                    layers.LSTM(128, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(out_seq_len)
                ])
            case '2':
                model = keras.Sequential([
                    layers.Input(shape=(None, X_train.shape[2])),
                    layers.LSTM(128, activation='relu', return_sequences=True),
                    layers.LSTM(64, activation='relu'),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(out_seq_len)
                ])

    if tf.config.list_physical_devices('GPU'):
        print("Using GPU for training")
    else:
        print("Using CPU for training")

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    early_stop = EarlyStopping(
        start_from_epoch=100,
        monitor='val_loss',
        patience=20,
        restore_best_weights=True
    )

    history = model.fit(
        X_train, y_train,
        epochs=300,
        batch_size=128,
        validation_split=0.05,
        verbose=1,
        callbacks=[early_stop]
    )

    loss, mae = model.evaluate(X_test, y_test)
    print(f"Test MAE: {mae:.4f}")

    model.save(
        f'{coin}_{modelName}_{mode}_{in_seq_len}_{out_seq_len}.keras'
    )
    return model


def load_model(mode, coin, model, in_seq_len, out_seq_len):
    try:
        model = keras.models.load_model(
            f'{coin}_{model}_{mode}_{in_seq_len}_{out_seq_len}.keras'
        )
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        print(f"Creating a new {model} model...")
        model = create_model(mode, coin, model, in_seq_len, out_seq_len)

    return model


def create_xminute_data(mode, coin):
    df = pd.read_csv(f'{coin}_order_book_summary.csv')
    shift_val = int(mode) - 1
    df[f'Price After {mode}min'] = df['Price After 1min'].shift(-shift_val)
    df.dropna(inplace=True)
    df.to_csv(f'{coin}_order_book_{mode}min_summary.csv')


def driver():
    mode = input(
        "Train for and predict next 1 min price or next x min price? Default is 1:\n"
    ).strip().lower() or '1'

    coin = input(
        "What coin do you want to predict? Default is btc:\n"
    ).strip().lower() or 'btc'

    modelName = input(
        "What model do you want to use? Default LSTM (options: MLP, LSTM):\n"
    ).strip().upper() or 'LSTM'

    modelName = modelName.upper()

    if modelName == 'LSTM':
        in_seq_len = input(
            "Enter the input sequence length (default 10):\n"
        ).strip() or '10'
        out_seq_len = input(
            "Enter the output sequence length (default 1):\n"
        ).strip() or '1'
    else:
        in_seq_len = '1'
        out_seq_len = '1'

    model = load_model(mode, coin, modelName, in_seq_len, out_seq_len)

    global mae
    if 'mae' not in globals():
        mae = 250 if coin == 'btc' else 0.0025

    print("\nStarting live prediction...\n")

    if modelName == 'LSTM' and int(in_seq_len) > 1:
        print(f"Gathering initial input data for {in_seq_len} minutes...")
        data_list = []

        for _ in range(int(in_seq_len) - 1):
            data_list.append(depth_chart_live(coin))
            time.sleep(60)

        data_list.append(depth_chart_live(coin))
        data_list = np.array(data_list)
        data = data_list.reshape(1, int(in_seq_len), data_list.shape[1])
    else:
        data = None

    while True:
        if modelName == 'MLP':
            data = depth_chart_live(coin)
            data = np.array(data).reshape(1, -1)
            prediction = model.predict(data)

            print(f"\nPredicted {coin} price for the next {mode} minute(s):")
            print(f"Prediction\t\t{prediction[0][0]:.3f}")
            print(f"Prediction - MAE\t{prediction[0][0] - mae:.3f}")
            print(f"Prediction + MAE\t{prediction[0][0] + mae:.3f}")
            print(f"Actual price now\t{get_coin_price(coin):.3f}")

        elif modelName == 'LSTM':
            if int(in_seq_len) == 1:
                data = depth_chart_live(coin)
                data = np.array(data).reshape(1, 1, -1)
            else:
                item = depth_chart_live(coin)
                item = np.array(item)
                data = np.concatenate(
                    (data[:, 1:, :], item.reshape(1, 1, item.shape[0])),
                    axis=1
                )

            prediction = model.predict(data)

            for i in range(len(prediction[0])):
                print(f"\nPredicted {coin} price for the next {int(mode) + i} minute(s):")
                print(f"Prediction\t\t{prediction[0][i]:.3f}")
                print(f"Prediction - MAE\t{prediction[0][i] - mae:.3f}")
                print(f"Prediction + MAE\t{prediction[0][i] + mae:.3f}")
                print(f"Actual price now\t{get_coin_price(coin):.3f}")
            print()

        time.sleep(60)


if __name__ == "__main__":
    driver()
