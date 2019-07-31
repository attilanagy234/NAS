
import torch
import numpy as np
from tensorboardX import SummaryWriter
import datetime
from trainer import Trainer
from utils import get_dataLoaders
# Install latest Tensorflow build
from tensorflow import summary


if __name__ == "__main__":
    # Seed for reproductivity
    torch.manual_seed(69)
    np.random.seed(360)

    current_time = datetime.datetime.now()
    writer = SummaryWriter("runs/" + str(current_time))

    # Hyperparameters
    batch_size = 64
    learning_rate_child = 0.01
    learning_rate_controller = 0.01
    momentum = 0.5
    l2_decay = 0
    param_per_layer = 4
    num_of_layers = 4
    input_dim = (28, 28)
    num_of_children = 10
    epoch_controller = 100
    epoch_child = 1
    entropy_weight = 0.000  # to encourage exploration
    log_interval = 5
    input_channels = 1
    output_dim = 10
    controller_size = 5
    controller_layers = 2

    # Data
    train_loader, test_loader = get_dataLoaders(batch_size, 1000)

    # Device
    use_cuda = False

    device = torch.device("cuda" if use_cuda else "cpu")

    trainer = Trainer(writer,
                      log_interval,
                      num_of_children,
                      input_channels,
                      output_dim,
                      learning_rate_child,
                      param_per_layer,
                      num_of_layers,
                      10,  # =out_filters, not used
                      controller_size,
                      controller_layers
                      )

    controller_optimizer = torch.optim.Adam(params=trainer.controller.parameters(),
                                            lr=learning_rate_controller,
                                            betas=(0.0, 0.999),
                                            eps=1e-3)

    val_acc = trainer.train_controller(trainer.controller,
                                       controller_optimizer,
                                       device,
                                       train_loader,
                                       test_loader,
                                       epoch_controller,
                                       momentum,
                                       entropy_weight)

    # writer.add_hparams(({"batch_size": 100,
    #                     "learning_rate_child": 0.01,
    #                     "learning_rate_controller": 0.01,
    #                     "momentum": 0.5,
    #                     "l2_decay": 0,
    #                     "param_per_layer": 4,
    #                     "num_of_layers": 2,
    #                     "input_dim": (28, 28),
    #                     "num_of_children": 3,
    #                     "epoch_controller": 3,
    #                     "epoch_child": 1,
    #                     "entropy_weight": 0.1,  # to encourage exploration
    #                     "log_interval": 5,
    #                     "input_channels": 1,
    #                     "controller_size": 5,
    #                     "output_dim": 10,
    #                     "controller_layers": 2},
    #                    {'hparam/accuracy': val_acc}))

    writer.close()
