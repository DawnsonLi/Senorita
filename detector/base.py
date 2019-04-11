# -*- coding=utf-8 -*-
import numpy as np
import pandas as pd
"""
there are some pratical methods for detecting anomaly in KPIs
"""
def stddev_from_ewma(X_recent, alpha = 0.3, coefficient = 3):
    """
    The basis for this detection is in a recent time window, such as 1 hour. 
    The curve follows a certain trend, and the new data points break the trend, 
    making the curve not smooth. That is to say, this detection utilizes the 
    temporal sequence of the time series, and T has a strong trend dependence 
    on T-1. To make an alarm based on recent trends, we need to fit the trend 
    of the curve. Here we use EWMA,The variance can be calculated after the 
    average value, and the variance is multiplied by a certain multiple to 
    obtain a tolerance range for the amplitude. If the actual value is beyond 
    this range, you can know if it can be alarmed.
    :param X: the time series to detect of
    :param type X: pandas.Series
    :param alpha: Discount rate of ewma, usually in (0.2, 0.3).
    :param coefficient: Coefficient is the width of the control limits, usually in (2.7, 3.0).
    :return: 1 denotes normal, 0 denotes abnormal
    """
    s = [X_recent[0]]
    for i in range(1, len(X_recent)):
        temp = alpha * X_recent[i] + (1 - alpha) * s[-1]
        s.append(temp)
    s_avg = np.mean(s)
    sigma = np.sqrt(np.var(X_recent))
    ucl = s_avg + coefficient * sigma * np.sqrt(alpha / (2 - alpha))
    lcl = s_avg - coefficient * sigma * np.sqrt(alpha / (2 - alpha))
    if s[-1] > ucl or s[-1] < lcl:
        return 0
    return 1

def recent_compare(X_recent, countnum = 25):
    """
    First, we can use the most recent time window. The data inside follows
    the trend of a certain trend. For example, if we set T to 7, we take 
    the detected value (nowvalue) and compare it with the last 7 (denoted 
    as i) points. If it is greater than the threshold, we will increase 
    the count by 1. If count exceeds the countnum we set, then it's considered
    as anomaly.Countnum can be set according to the requirements. For example,
    it is sensitive to exceptions. You can set countnum to be smaller. If 
    it is not sensitive to exceptions, you can set countnum to be larger.
    :param X_recent: the time series window
    :param type X: pandas.Series
    :param countnum: parameter to adjust anomaly
    """
    tmp = X_recent[: len(X_recent)-1]
    AVG = np.mean(tmp)
    MAX = max(tmp)
    MIN = min(tmp) 
    thred = min(MAX - AVG, AVG - MIN)
    su = 0
    for t in tmp:
        if  X_recent[-1] - t > thred:
            su += 1
    if su>= countnum:
        return 0
    return 1

def tail_compare(X_recent):
    """
    Calcuate the simple average over recent data.
    A X_recent is anomalous if the average of the last three datapoints
    are outside of three standard deviations of this value.
    """
    if len(X_recent)<5:
        raise RuntimeError('the data used for API tail_compare can not less than 5')
    AVG = np.mean(X_recent)
    stdDev = np.std(X_recent)
    t = (X_recent[-1] + X_recent[-2] + X_recent[-3] )/3
    if abs(t - AVG) > 3 * stdDev:
        return 0
    else:
        return 1
    
def absolute_periodicity_min(X_14, coefficient = 0.6):
    """
    name: Time periodicity based on absolute value
    formula: 
    min(14 days history) * 0.6
    Take the minimum value for the historical 14-day curve. How do you get the minimum value? 
    For 12:05, there are 14 corresponding points, taking the minimum. For 12:06, there are 14 
    corresponding points, taking the minimum. This will give you a curve of the day. Then multiply 
    this curve by 0.6 as a whole. If the curve for a few days is lower than this reference line, 
    it will alarm. This is actually an upgraded version of a static threshold alarm, a dynamic 
    threshold alarm. In the past, the static threshold was a product of a brain based on historical 
    experience. Using this algorithm, in fact, based on the historical value of the point at the 
    same time, calculate the most unlikely lower bound. At the same time, the threshold is not
    the only one, but one at each time. If there is a point in 1 minute, there are 1440 lower bound
    thresholds in one day. Of course, the actual use of 0.6 should still be adjusted as appropriate. 
    And a serious problem is that if there is a downtime release or failure in the 14-day history,
    then the minimum will be affected. In other words, history cannot be regarded as normal, but 
    the history must be removed from the outliers before calculation. A pragmatic approximation 
    is to take the second smallest value.
    :param X_14: the time series to detect of 14 days, note that X_14 could be larger than 14
    :param type X: pandas.Series
    :param coefficient: 0.6 in the formula
    :return: 1 denotes normal, 0 denotes abnormal
    """
    tmp = X_14[: len(X_14)-1]
    tmp.sort()
    if tmp[1] >= 0:
        lcl = tmp[1] *coefficient #use the second smallest
    else:
        lcl = tmp[1] * (2-coefficient)
    
    if X_14[-1] < lcl:
        #print lcl,"*",tmp[1],X_14
        return 0
    else:
        return 1
    
def absolute_periodicity_max(X_14, coefficient = 1.4):
    """
    reference to the api absolute_periodicity_min
    """
    tmp = X_14[: len(X_14)-1]
    ucl = np.max(tmp)*coefficient
    if X_14[-1] > ucl:
        return 0
    else:
        return 1
    
def amplitude_periodicity(X_14):
    """
    Sometimes the curve has periodicity, but the superposition of the curves of 
    the two cycles is not coincident. For example, the above trend, the overall 
    trend of the curve is online. The curves of the two cycles are superimposed 
    one on top of the other, and one will be higher than the other. In this case, 
    there is a problem with the use of absolute value alarms. For example, today 
    is 10.1 days, the first day of the holiday. The historical curve of the past 
    14 days is bound to be much lower than today's curve. Then there was a glitch 
    today, the curve fell, and the curve relative to the past 14 days is still much
    higher. How can such a fault be detected? An intuitive statement is that although
    the two curves are not the same, they are "almost like." So how do you use this
    "almost like"? That is the amplitude. Instead of using the value of x(t), use 
    the value of x(t) – x(t-1), that is, change the absolute value to the rate of change.
    There are two tricks in practice: it can be x(t) – x(t-1) or x(t) – x(t-5). 
    The larger the span, the more you can detect some slow declines.Another trick 
    is to calculate x(t) -x(t-2), and x(t+1) – x(t-1). If both values are abnormal, 
    it is considered to be a true exception, and a point can be avoided
    """
    dif1 = [X_14[i] - X_14[i-1] for i in range(1, len(X_14))]
    
    #dif5 = [X_14[i] - X_14[i-5] for i in range(5, len(X_14))]
    if absolute_periodicity_min(dif1) > 0:
        return 1
    return 0


