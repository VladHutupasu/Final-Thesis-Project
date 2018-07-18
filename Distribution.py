import pandas as pd
import numpy as np
import operator
import heapq
import matplotlib.pyplot as plt
from scipy.stats import norm


def closeOverTime(market_info):
    market_info.Close.plot(logy=True)
    plt.legend()
    plt.show()

def returnHist(market_info, nBiggestProbabilities):

    # Trying to fit the returns to a normal distribution
    parameters = norm.fit(market_info.Returns - 1)

    # now, parameters[0] and parameters[1] are the mean and the standard deviation of the fitted distribution
    x = np.linspace(min(market_info.Returns - 1), max(market_info.Returns - 1), 100)

    # Generate the pdf (fitted distribution)
    fitted_pdf = norm.pdf(x, loc=parameters[0], scale=parameters[1])

    # Plot the distribution and histogram for the Returns
    plt.plot(x,fitted_pdf,"red",label="Normal distribution",linestyle="dashed", linewidth=2)
    plt.hist((market_info.Returns-1),density=1,color="b",alpha=.3, bins=10, label='Daily returns')
    plt.title("Bitcoin distribution in Returns")
    plt.legend()
    # plt.show()

    percentages = []
    probabilities = []


    for x in ((market_info.Returns-1)*100):
        percentages.append(round(x, 1))

    w = np.linspace(-25, 25, 501)
    for i in range(len(w)):
        w[i] = round(w[i], 1)


    dictPercProb={}
    dictFinal={}

    for i in w:
        probabilities.append(percentages.count(i)/len(percentages)*100)
        # print("Chance for the price to go "+str(i)+"% is ->"+str(percentages.count(i)/len(percentages)*100)+"%")
        dictPercProb[i]=(percentages.count(i)/len(percentages)*100)


    largestProb = heapq.nlargest(nBiggestProbabilities, probabilities)

    print("\n----------The n biggest probabilities----------")

    for j in range(len(largestProb)):
        for w in range(len(dictPercProb)):
            if(dictPercProb[list(dictPercProb.keys())[w]] == largestProb[j]):
                dictFinal[list(dictPercProb.keys())[w]] = largestProb[j]

    sorted_x = sorted(dictFinal.items(), key=operator.itemgetter(0))
    print(sorted_x)
    print('Movement between: '+str(sorted_x[0][0])+' -> '+str(sorted_x[len(sorted_x)-1][0]))
    return sorted_x





def showDist(start_date, end_date, nBiggestProbabilities):

    # using the hourly data for June July, since we trade in that period
    bitcoin_market_info = pd.read_csv(r'hourly data/June - July hourly data.csv')

    market_info = bitcoin_market_info

    # filter the requested data
    market_info = market_info[market_info['Date'] <= end_date]
    market_info = market_info[market_info['Date'] >= start_date]


    market_info.index = pd.to_datetime(market_info.Date)
    market_info = market_info.drop(['Date'], axis=1)
    market_info = market_info[['Close']]


    market_info.columns = ['Close']
    market_info['Close'].replace(0, np.nan, inplace=True)
    market_info = market_info.dropna()

    # create returns column
    market_info['Returns'] = (market_info['Close'].pct_change() + 1).fillna(1)

    # use this method to see the evolution of price
    # closeOverTime(market_info)

    return returnHist(market_info, nBiggestProbabilities)












