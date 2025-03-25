import random
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

### Data Loading: Sequence Dataset
class SequenceDataset(Dataset):
    def __init__(self, file_list, stmsize, imsize, length):
        # file_list: List of image file paths, assumed to be ordered in time.
        # stmsize: Number of consecutive images to form one sequence (how many days prior should the model consider?)
        # imsize: The size of the cropped region (imsize x imsize).
        # length: The size to which each image is resized before cropping.
        self.file_list = sorted(file_list)
        self.stmsize = stmsize
        self.imsize = imsize
        self.length = length
        self.num_samples = len(self.file_list) - stmsize + 1  # Total number of sequences available.

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Randomly choose a crop location that will be consistent for all images in the sequence.
        x0 = random.randint(0, self.length - self.imsize)
        y0 = random.randint(0, self.length - self.imsize)
        sequence = []
        for i in range(idx, idx + self.stmsize):
            # Read the image in grayscale.
            img = cv2.imread(self.file_list[i], cv2.IMREAD_GRAYSCALE)
            # Resize image to a fixed square (length x length).
            img = cv2.resize(img, (self.length, self.length))
            # Crop a region of size (imsize x imsize) from the resized image.
            crop = img[x0:x0+self.imsize, y0:y0+self.imsize]
            # Normalize pixel values to [0,1].
            crop = crop.astype(np.float32) / 255.0
            # Add a new channel dimension (for compatibility with convolutional layers).
            sequence.append(crop[np.newaxis, ...])
        # Stack the sequence along the channel axis.
        sample = np.concatenate(sequence, axis=0)
        # If the sequence has fewer channels than expected (here expected is 50), pad with zeros.
        # This allows the model (which expects 50 input channels) to work even if stmsize is lower.
        if sample.shape[0] < 50:
            pad_channels = 50 - sample.shape[0]
            padding = np.zeros((pad_channels, self.imsize, self.imsize), dtype=np.float32)
            sample = np.concatenate([sample, padding], axis=0)
        return torch.from_numpy(sample)

### Model Architecture: ULSTM
class ULSTM(nn.Module):
    def __init__(self):
        super(ULSTM, self).__init__()
        # Encoder: Three convolutional layers to extract spatial features.
        # Input channels are 50 (as expected from the dataset after padding).
        self.conv1 = nn.Conv2d(in_channels=50, out_channels=8, kernel_size=5, stride=1)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=8, kernel_size=5, stride=1)
        self.conv3 = nn.Conv2d(in_channels=8, out_channels=8, kernel_size=5, stride=1)
        # Batch normalization helps in stabilizing the training.
        self.norm1 = nn.BatchNorm2d(8)
        self.norm2 = nn.BatchNorm2d(8)
        # Average pooling layers reduce spatial dimensions.
        self.down1 = nn.AvgPool2d(2)
        self.down2 = nn.AvgPool2d(2)
        self.down3 = nn.AvgPool2d(2)
        
        # LSTM layer: processes flattened spatial features.
        # Here, after three poolings, we assume the spatial dimensions are lstmin x lstmin.
        self.lstmin = 21
        self.lstmout = 32
        self.lstm1 = nn.LSTM(
            input_size=self.lstmin * self.lstmin,  # Flattened features per channel.
            hidden_size=self.lstmout * self.lstmout, # LSTM output size (reshaped later into spatial dimensions).
            num_layers=2,
        )
        
        # Decoder: Deconvolution layers to upsample and reconstruct the output.
        self.deconv1 = nn.Conv2d(in_channels=8, out_channels=8, kernel_size=5, stride=1)
        self.deconv2 = nn.Conv2d(in_channels=8, out_channels=8, kernel_size=5, stride=1)
        self.deconv3 = nn.Conv2d(in_channels=8, out_channels=1, kernel_size=5, stride=1)
        # Batch normalization for decoder.
        self.dnorm1 = nn.BatchNorm2d(8)
        self.dnorm2 = nn.BatchNorm2d(8)
        # Upsampling layers to recover spatial dimensions.
        self.up1 = nn.UpsamplingBilinear2d(scale_factor=2)
        self.up2 = nn.UpsamplingBilinear2d(scale_factor=2)
        self.up3 = nn.UpsamplingBilinear2d(scale_factor=2)
        
        # Final activation function to squash outputs between 0 and 1.
        self.activation = nn.Sigmoid()

    def forward(self, x):
        # Encoder forward pass.
        x = F.relu(self.conv1(x))
        x = self.down1(x)
        x = self.norm1(x)
        x = F.relu(self.conv2(x))
        x = self.down2(x)
        x = self.norm2(x)
        x = F.relu(self.conv3(x))
        x = self.down3(x)
        
        # Flatten spatial dimensions to feed into the LSTM.
        b, c, h, w = x.size()
        x = x.view(b, c, h * w)
        # Process with LSTM; output shape remains [batch, c, h*w].
        x, _ = self.lstm1(x)
        # Reshape LSTM output back to spatial dimensions.
        x = x.view(b, c, self.lstmout, self.lstmout)
        
        # Decoder forward pass.
        x = self.deconv1(x)
        x = self.up1(x)
        x = self.dnorm1(x)
        x = self.deconv2(x)
        x = self.up2(x)
        x = self.dnorm2(x)
        x = self.deconv3(x)
        x = self.up3(x)
        return self.activation(x)
