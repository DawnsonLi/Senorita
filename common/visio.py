# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(df):
    anomaly = df[df['label']==1]
    normal = df[df['label']==0]
    ax1 = anomaly.plot.scatter(x='timestamp', y='value', color='b', marker='s', label='anomaly') 
    ax2 = normal.plot.scatter(x='timestamp', y='value', color='g', alpha=0.2, label='normal', ax=ax1)
    plt.xlabel('timestamp', fontsize = 20)
    plt.ylabel('value', fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.show()
def plot_anomaly(df):
    ax1 = df.plot(x='timestamp', y='value', color='g')
    anomaly = df[df['label']==1]
    anomaly.plot.scatter(x='timestamp', y='value', color='b', marker='s', label='anomaly', ax = ax1) 
    plt.xlabel('timestamp', fontsize = 20)
    plt.ylabel('value', fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.show()
def truth_predict(real, predict):
    ans = []
    for i in range(len(predict)):
        if real[i] == 1 and predict[i] == 1:
            ans.append(1)#tp
        elif real[i] == 1 and predict[i] == 0:#not find anomaly       
            ans.append(2)#fn
        elif real[i] ==0 and predict[i]==0:    
            ans.append(3)#tn
        else:
            ans.append(4)#fp
    
    return ans    
        
def evalute(real, predict):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(predict)):
        if real[i] == 1 and predict[i] == 1:
            tp += 1
        elif real[i] == 1 and predict[i] == 0:#not find anomaly       
            fn += 1
        elif real[i] ==0 and predict[i]==0:    
            tn += 1
        else:
            fp += 1
    print 'TP',tp 
    print 'TN',tn 
    print 'FP',fp 
    print 'FN',fn
    precison = 0
    recall = 0
    f1 =0
    if tp+fp > 0:
        precison = tp*1.0/(tp+fp)
    if tp+fn>0:
        recall = tp*1.0/(tp+fn)
    if precison+recall>0:
        f1 = 2*precison*recall/(precison+recall)  
    print 'precison',precison
    print 'recall',recall
    print 'f1',f1
def plot_ans(df, predict,ratio = 1):
    real = df['label'].values
    evalute(real, predict)
    print real[:100]
    print predict[:100]
    df['y'] = pd.Series(truth_predict(real, predict))
    df = df[:len(df)/ratio]#容易导致后续四个dataframe为空而报错
    tp = df[df['y'] == 1]
    fn = df[df['y'] == 2]
    tn = df[df['y'] == 3]
    fp = df[df['y'] == 4]
    try:
        if len(fn) >0 and len(fp) >0:
            ax = tp.plot.scatter(x='timestamp', y='value', color='b', label='tp') 
            ax1 = tn.plot.scatter(x='timestamp',y = 'value', color = 'g',alpha = 0.15, ax =ax, label='tn')  
            ax2= fn.plot.scatter(x='timestamp', y='value', color='b',marker='x', label='fn', ax=ax1)
            fp.plot.scatter(x='timestamp',y = 'value', color = 'r', marker = 'x',ax =ax2, label='fp')
            plt.show()
        elif len(fn) > 0: #fp = 0
            ax = tp.plot.scatter(x='timestamp', y='value', color='b', label='tp') 
            ax1 = tn.plot.scatter(x='timestamp',y = 'value', color = 'g',alpha = 0.15, ax =ax, label='tn')  
            fn.plot.scatter(x='timestamp', y='value', color='b',marker='x', label='fn', ax=ax1)
            plt.show()
        elif len(fp) >0: #fn=0
            ax = tp.plot.scatter(x='timestamp', y='value', color='b', label='tp') 
            ax1 = tn.plot.scatter(x='timestamp',y = 'value', color = 'g',alpha = 0.15, ax =ax, label='tn')  
            fp.plot.scatter(x='timestamp',y = 'value', color = 'r', marker = 'x',ax =ax1, label='fp')
            plt.show()   
        else:
            ax = tp.plot.scatter(x='timestamp', y='value', color='b', label='tp') 
            tn.plot.scatter(x='timestamp',y = 'value', color = 'g',alpha = 0.15, ax =ax, label='tn')  
            plt.show()
    except ValueError:
        print 'can not plot cause there is one or more 0 in TP,TN,FP,FN'