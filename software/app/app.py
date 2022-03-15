from webbrowser import get
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet
from bitcoinlib.keys import HDKey
from bitcoinlib.keys import Key
from dotenv import load_dotenv
from appJar import gui
from appJar.appjar import WIDGET_NAMES
import datetime
import requests
import serial
import random
import string
import qrcode
import json
import time
import os


if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')


def log(msg):
    if (msg == ''): return
    day = f"{datetime.datetime.now():%d}"
    month = f"{datetime.datetime.now():%m}"
    logDir = f'./logs/{month}/'
    logFile = f'./logs/{month}/{day}.txt'
    if not (os.path.isdir(logDir)):
        os.mkdir(logDir)
    logFileObject = open(logFile, 'a')
    logLine = f'[{datetime.datetime.now():%Y-%m-%d %I:%M:%S}] {msg} \n';
    logFileObject.write(logLine)
    logFileObject.close()
    print(logLine)


load_dotenv()
log('Starting...')
time.sleep(10)
log('Started')
permiumRate = float(os.environ.get('PREMIUM', '0.02'))
credit = 0
credit_ = 0
shouldPrint = False
apex = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

btc = False
btcBuyPrice = False
while not (btc and btcBuyPrice):
    try:
        btcValueRequest = requests.get(f'https://blockchain.info/tobtc?currency=USD&value=1')
        btc = float(btcValueRequest.text)
        btcBuyPriceRequest = requests.get(f'https://blockchain.info/ticker')
        ticker = json.loads(btcBuyPriceRequest.text)
        btcBuyPrice = ticker['USD']['buy']
        log(f'$1 USD = ₿ {btc}')
        log(f'₿ 1 = $USD {str(btcBuyPrice)}')
    except:
        print("An exception occurred while getting BTC Prices")
        time.sleep(5)



app = gui("ATM", os.environ.get('DISPLAY_SIZE', 'fullscreen'))

walletName = 'MAIN-'+''.join(random.choices(string.ascii_lowercase, k=10))
seed = Mnemonic().to_seed(os.environ.get('MAIN_SEED')).hex()
mainKey = HDKey().from_seed(seed)
mainWallet = Wallet.create(walletName, mainKey)
mainWallet.scan(scan_gap_limit=5)
balance = str(mainWallet.balance())
log(f'Balance: ₿{balance}')
log(f'Balance: ₿{balance}')

def serialLoop(): 
    global shouldPrint
    global credit
    global btc

    if (shouldPrint):
        shouldPrint = False
        printWallet()

    input = apex.readline().decode("utf-8").rstrip().lstrip()
    log(input)
    
    if (input == '$1 Credit'):
        credit = credit + 1
        print(credit)
    if (input == '$5 Credit'):
        credit = credit + 5
        print(credit)
    if (input == '$10 Credit'):
        credit = credit + 10
        print(credit)
    if (input == '$20 Credit'):
        credit = credit + 20
        print(credit)
    if (input == '$50 Credit'):
        credit = credit + 50
        print(credit)
    if (input == '$100 Credit'):
        credit = credit + 100
        print(credit)
    
    if (credit > 0):
        app.setFont(size=70)
        app.setLabel('permium', 'Premium: ' + str(permiumRate*100) + '%')
        app.setLabel('usd', '$'+str(credit))
        credit_ = credit - (credit * permiumRate)
        btc_ = btc*credit_
        app.setLabel('btc', f'≈ ₿{btc_:.8f}')
        
    if (input == 'PRINT'):
        app.hideWidgetType(WIDGET_NAMES.Label, 'usd')
        app.hideWidgetType(WIDGET_NAMES.Label, 'permium')
        app.setLabel('btc', f'Printing...')
        shouldPrint = True
        # printWallet()
    
def printWallet():
    global btcBuyPrice
    global credit
    
    credit_ = creditSubtractPremium()
    btcCreditValueRequest = requests.get(f'https://blockchain.info/tobtc?currency=USD&value={credit_}')
    btc_ = btcCreditValueRequest.text
    log(f'credit: {credit}')
    log(f'crediwtSubtractPremium: {credit_}')
    log(f'profit: {credit - credit_}')
    log(f'creditSubtractPremium as BTC: {btc_}')
    outputName = ''.join(random.choices(string.ascii_lowercase, k=10))

    k = Key()
    address = k.address()
    privateKey = k.wif()
    # txString = "2d41fcd88e5659190de828ab0d4116edf1d711306740e5d425d22cc805c6fe7d"
    tx = mainWallet.send_to(address, str(btc_)+' BTC')
    tx.info()
    txString = ""
    export = tx.export()
    if (export[0]):
        txString = export[0][1]
    
    os.system(f'mkdir -p ./output/{outputName}')
    os.system(f'cp ./wallet/index.html ./output/{outputName}')
    os.system(f'cp ./wallet/background.jpeg ./output/{outputName}')
    os.system(f'cp ./wallet/ticketing.ttf ./output/{outputName}')

    publicKeyQR = qrcode.make(address)
    publicKeyQR.save(f'./output/{outputName}/public.png')
    statusQR = qrcode.make(f'https://www.blockchain.com/btc/tx/{txString}')
    statusQR.save(f'./output/{outputName}/status.png')
    privateKeyQR = qrcode.make(privateKey)
    privateKeyQR.save(f'./output/{outputName}/private.png')

    with open(f'./output/{outputName}/index.html', 'r') as file:
        data = file.read()
        data = data.replace('[BTC]', f'₿{float(btc_):.8f}')
        data = data.replace('[CURRENCY]', 'BITCOIN')
        data = data.replace('[TIME]', f"{datetime.datetime.now():%I:%M:%S}")
        data = data.replace('[DATE]', f"{datetime.datetime.now():%Y-%m-%d}")
        data = data.replace('[ADDRESS]', address)
        data = data.replace('[TX]', txString)
        data = data.replace('[ADDRESS]', address)
        data = data.replace('[PRIVATE_KEY]', privateKey)
    with open(f'./output/{outputName}/index.html', 'w') as file:
        file.write(data)

    os.system(f'wkhtmltopdf -q --page-height 150 --page-width 100 -O Landscape ./output/{outputName}/index.html ./output/{outputName}/wallet.pdf')
    os.system(f'lp -h localhost:631 ./output/{outputName}/wallet.pdf')
    time.sleep(1)
    apex.flush()
    credit = 0;
    app.setFont(size=50)
    app.showWidgetType(WIDGET_NAMES.Label, 'usd')
    app.setLabel('usd', 'Open-Source Bitcoin ATM')
    app.setLabel('btc', 'Insert Cash To Begin')
    apex.write(b"RESET\n")
    apex.flush()
    time.sleep(1)
    os.system(f'rm -rf ./output/{outputName}')
    updateBTCBuyPriceRequest = requests.get(f'https://blockchain.info/ticker')
    ticker = json.loads(updateBTCBuyPriceRequest.text)
    btcBuyPrice = ticker['USD']['buy']
    app.setLabel('permium', '1 BTC = $' + str(btcBuyPrice))
    app.showWidgetType(WIDGET_NAMES.Label, 'permium')
    
    # Update Balance
    mainWallet.scan(scan_gap_limit=5)
    mainWallet.transactions_update_confirmations()
    balance = str(mainWallet.balance())
    log(f'Balance: ₿{balance}')

def creditSubtractPremium():
    global credit
    credit_ = credit - (credit * permiumRate)
    return credit_

app.setFont(size=50)
app.setBg("#292D39")
app.setFg("white")
app.registerEvent(serialLoop)
app.setStretch('both')
app.setSticky('news')
app.addLabel('usd', 'Open-Source Bitcoin ATM')
app.addLabel('btc', 'Insert Cash To Begin')
app.addLabel('permium', '1 BTC = $' + str(btcBuyPrice))
app.go()
