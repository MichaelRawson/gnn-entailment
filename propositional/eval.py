#!/usr/bin/env python3
import torch
from torch.nn.functional import binary_cross_entropy_with_logits
from torch_geometric.data import Batch
from tqdm import tqdm

from common import mk_loader
from dataset import LogicalEntailmentDataset
from model import Model
from statistics import Writer

def accuracy(model, data):
    total = 0
    correct = 0
    with torch.no_grad():
        for batch in tqdm(data):
            batch = batch.to('cuda')
            actual = batch.y
            predicted = torch.sigmoid(model(batch)).round().long()
            correct += actual.eq(predicted).sum().item()
            total += len(predicted)
            del batch

    return 100 * (correct / total)

def eval():
    validation = mk_loader('data', 'validate.txt')
    test_easy = mk_loader('data', 'test_easy.txt')
    test_hard = mk_loader('data', 'test_hard.txt')
    test_big = mk_loader('data', 'test_big.txt')
    test_massive = mk_loader('data', 'test_massive.txt')
    test_exam = mk_loader('data', 'test_exam.txt')

    model = Model(4).to('cuda')
    model.load_state_dict(torch.load('model.pt'))
    model.eval()

    val_acc = accuracy(model, validation)
    test_easy_acc = accuracy(model, test_easy)
    test_hard_acc = accuracy(model, test_hard)
    test_big_acc = accuracy(model, test_big)
    test_massive_acc = accuracy(model, test_massive)
    test_exam_acc = accuracy(model, test_exam)

    print(f"validation:\t{val_acc:.1f}%")
    print(f"test (easy):\t{test_easy_acc:.1f}%")
    print(f"test (hard):\t{test_hard_acc:.1f}%")
    print(f"test (big):\t{test_big_acc:.1f}%")
    print(f"test (massive):\t{test_massive_acc:.1f}%")
    print(f"test (exam):\t{test_exam_acc:.1f}%")

if __name__ == '__main__':
    torch.manual_seed(0)
    eval()
