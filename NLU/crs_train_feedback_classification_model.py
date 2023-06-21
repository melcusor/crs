import pathlib
from datetime import datetime
import torch
import re
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics
from torch.optim import Adam
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from torch import nn
from crs_transformers_bert_sentiment_classifier import BertClassifier
from transformers import AutoTokenizer


fb_data_file_path = "C:/Users/emale/Documents/uni/MA/conv_rec_sys_food/NLU/samples_feedback_classification/"
#fd_data_file_name = "v_20230207_feedback_labels_lower_upper_combined.csv"
#fd_data_file_name = "v_20230207_feedback_labels.csv"
#fd_data_file_name = "v_20230208_feedback_labels.csv"
fd_data_file_name = "v_20230208_feedback_labels_lower_upper_combined.csv"

train_size = 0.8
test_batch_size = 1

# 2nd option: "oliverguhr/german-sentiment-bert"
pretrained_model = 'bert-base-german-cased'
tokenizer = AutoTokenizer.from_pretrained(pretrained_model)

padding_max_length = 32
batch_size = 64
epochs = 10
lr = 1e-4
dropout = 0.5
# model_name = "oliverguhr-german-sentiment-bert" + str(datetime.now().strftime("%Y%m%d_%H%M%S"))
model_name = "bert-base-german-cased-bert" + str(datetime.now().strftime("%Y%m%d_%H%M%S"))
model_file_path = "C:/Users/emale/Documents/uni/MA/conv_rec_sys_food/NLU/saved-models/"

_save_plot = True


class Dataset(torch.utils.data.Dataset):
    def __init__(self, df):

        self.labels = list(df.feedback_code)
        self.texts = [tokenizer(text, padding='max_length', max_length=padding_max_length, truncation=True,
                                return_tensors="pt") for text in df['text']]

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        # Fetch a batch of inputs
        return self.texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y


def _read_fb_file(file):
    fb_df = pd.read_csv(file, sep=",", header=0)
    return fb_df


def train(model, train_data, val_data, learning_rate, epochs):
    train_set, val_set = Dataset(train_data), Dataset(val_data)

    train_dataloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_dataloader = torch.utils.data.DataLoader(val_set, batch_size=batch_size)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    print("Device: ", device)

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=learning_rate)

    if use_cuda:
        print("Using CUDA!")
        model = model.cuda()
        criterion = criterion.cuda()

    train_losses_for_plot = []
    train_accuracy_for_plot = []

    val_losses_for_plot = []
    val_accuracy_for_plot = []

    for epoch_num in range(epochs):
        total_acc_train = 0
        total_loss_train = 0

        for train_input, train_label in tqdm(train_dataloader):
            train_label = train_label.to(device)
            mask = train_input['attention_mask'].to(device)
            input_id = train_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)

            batch_loss = criterion(output, train_label.long())
            total_loss_train += batch_loss.item()

            acc = (output.argmax(dim=1) == train_label).sum().item()
            total_acc_train += acc

            model.zero_grad()
            batch_loss.backward()
            optimizer.step()

        train_epoch_loss = total_loss_train / len(train_data)
        train_epoch_accuracy = total_acc_train / len(train_data)
        train_losses_for_plot.append(train_epoch_loss)
        train_accuracy_for_plot.append(train_epoch_accuracy)

        total_acc_val = 0
        total_loss_val = 0

        with torch.no_grad():

            for val_input, val_label in val_dataloader:
                val_label = val_label.to(device)
                mask = val_input['attention_mask'].to(device)
                input_id = val_input['input_ids'].squeeze(1).to(device)

                output = model(input_id, mask)

                batch_loss = criterion(output, val_label.long())
                total_loss_val += batch_loss.item()

                acc = (output.argmax(dim=1) == val_label).sum().item()
                total_acc_val += acc

        val_epoch_loss = total_loss_val / len(val_data)
        val_epoch_accuracy = total_acc_val / len(val_data)
        val_losses_for_plot.append(val_epoch_loss)
        val_accuracy_for_plot.append(val_epoch_accuracy)

        print(
            f'Epochs: {epoch_num + 1} | Train Loss: {train_epoch_loss: .4f} \
            | Train Accuracy: {train_epoch_accuracy: .4f} \
            | Val Loss: {val_epoch_loss: .4f} \
            | Val Accuracy: {val_epoch_accuracy: .4f}')

    fig = plt.figure(figsize=(15, 10))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(np.linspace(1, epochs, epochs).astype(int), train_losses_for_plot, alpha=1, c="darkblue", lw=1.2,
             ls="dashed", label="Training Loss")
    ax1.plot(np.linspace(1, epochs, epochs).astype(int), val_losses_for_plot, alpha=0.9, c="limegreen", lw=1,
             label="Validation Loss")
    ax1.set_title("Train/Validation Epoch Loss")
    ax1.legend()

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(np.linspace(1, epochs, epochs).astype(int), train_accuracy_for_plot, alpha=1, c="darkblue", lw=1.2,
             ls="dashed", label="Train Accuracy")
    ax2.plot(np.linspace(1, epochs, epochs).astype(int), val_accuracy_for_plot, alpha=0.9, c="limegreen", lw=1,
             label="Validation Accuracy")
    ax2.set_title("Train/Validation Epoch Accuracy")
    ax2.legend()

    ax1.grid(which="both")
    ax2.grid(which="both")

    if _save_plot:
        image_name = "loss_acc_" + model_name + '.png'
        abspath = pathlib.Path(image_name).absolute()
        plt.savefig(abspath)
    # plt.show()


def evaluate(model, test_data):
    test = Dataset(test_data)
    print("len test classes: ", len(test.classes()))
    y_actual = np.array(test.classes())
    # TEST BATCH SIZE: https://ai.stackexchange.com/questions/10201/what-is-the-reason-behind-using-a-test-batch-size
    # [09.12.2022]
    test_dataloader = torch.utils.data.DataLoader(test, batch_size=test_batch_size)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    if use_cuda:
        model = model.cuda()

    total_acc_test = 0

    y_pred = np.empty((1), dtype=int)

    with torch.no_grad():

        for test_input, test_label in test_dataloader:
            test_label = test_label.to(device)
            mask = test_input['attention_mask'].to(device)
            input_id = test_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)

            acc = (output.argmax(dim=1) == test_label).sum().item()
            # print("Argmax: ", output.argmax(dim=1), "test_label", test_label, "accuracy: ", acc)

            y_pred = np.concatenate((y_pred, output.argmax(dim=1).cpu().numpy()))
            # print("y_pred during eval: ", y_pred)

            total_acc_test += acc

    avg_test_accuracy = total_acc_test / len(test_data)
    print('avg_test_accuracy: ', round(avg_test_accuracy, 3))

    # print(y_pred.shape)
    # print(y_pred)
    # print("no_correct_labels", np.equal(np.delete(y_actual, 0), np.delete(y_pred, 0)).sum())

    y_pred = np.delete(y_pred, 0)
    # print(y_pred.shape)

    print("Classification_report: ", metrics.classification_report(y_actual, y_pred))
    f1_score = metrics.f1_score(y_actual, y_pred, average="weighted")
    print("avg_test_f1_score: ", f1_score)

    # https://towardsdatascience.com/comprehensive-guide-to-multiclass-classification-with-sklearn-127cc500f362 [28.11.2022]
    fig, ax = plt.subplots(figsize=(12, 8))

    cm = metrics.confusion_matrix(y_actual, y_pred)
    print(pd.DataFrame(cm))
    cmp = metrics.ConfusionMatrixDisplay(cm)
    cmp.plot(ax=ax)

    if _save_plot:
        image_name = "conf_matrix_" + model_name + '.png'
        abspath = pathlib.Path(image_name).absolute()
        plt.savefig(abspath)
    # plt.show()


def save_model(model):
    # file_name = model_file_path + model_name
    file_name = model_name + f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    abspath = pathlib.Path(file_name).absolute()
    torch.save(model.state_dict(), str(abspath))


def main():

    print("Reading fb files...")
    fb_df = _read_fb_file(fb_data_file_path + fd_data_file_name)
    fb_df = fb_df[["text", "feedback_code"]]
    # pd.set_option('display.max_columns', None)
    # print(fb_df.head())
    # print(fb_df.feedback_code.value_counts())
    np.random.seed(814)

    second_split_limit = train_size + (1-train_size)/2

    df_train, df_val, df_test = np.split(fb_df.sample(frac=1, random_state=612),
                                         [int(train_size * len(fb_df)), int(second_split_limit * len(fb_df))])
    df_test.to_csv("fb_test.csv", index=None)

    print("train_length:", len(df_train))
    print("validate_length:", len(df_val))
    print("test_length: ", len(df_test))

    print("train_counts:", df_train.feedback_code.value_counts())
    print("val_counts:", df_val.feedback_code.value_counts())
    print("test_counts:", df_test.feedback_code.value_counts())

    model = BertClassifier(dropout=dropout)

    train(model, df_train, df_val, lr, epochs)
    evaluate(model, df_test)

    save_model(model)


if __name__ == '__main__':
    main()
