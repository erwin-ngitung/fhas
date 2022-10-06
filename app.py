from streamlit_multipage import MultiPage
from tools import anomaly_detection as dt
from tools import processing_data as pdt
from tools import building_model as bd
from tools import check_email
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")

