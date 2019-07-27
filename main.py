from net_manager import NetManager
from child import Child
from torchvision import datasets, transforms
import torch

if __name__ == "__main__":
    '''
    data_loader = DataLoader(path)
    data = dataLoader.load_data()
    net_manager = NetManager()
    net_manager.start(data)
    '''

    use_cuda = False
    device = torch.device("cuda" if use_cuda else "cpu")


    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=64, shuffle=True)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=1000, shuffle=True)

    netmanager = NetManager(5, 5, 1, 5, 5, 5, 2, 5)
    conf = netmanager.make_config("2 3 4 5 6 2 3 4 5 6")
    child = Child(conf, 0.01, 0.04, 10)
    print(str(child))
    for epoch_idx in range(4):
        netmanager.train_child(child, device, train_loader, 1)
        netmanager.test_child(child, device, test_loader)

