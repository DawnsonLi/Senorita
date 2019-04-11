# Senorita
<360和腾讯公司> KPI实用异常检测算法实现
## 简介
这里的算法偏向启发式，比如阈值的设定，算法的设计等，同时算法面向实际，简单但高效
## 算法介绍(detector下)

### stddev_from_ewma

>这种检测的根据是在一个最近的时间窗口，比如1个小时内，曲线会遵循某种趋势，而新的数据点打破了这种趋势，使得曲线不光滑了。也就是说，这种检测利用的是时间序列的temporal dependency，T对于T-1有很强的趋势依赖性。业务逻辑上来说，8:00 有很多人登陆，8:01 也有很多人来登陆的概率是很高的，因为吸引人来登陆的因素是有很强的惯性的。但是7.1很多人来登陆，8.1也有很多人来登陆的惯性就要差很多。 <br>
>基于近期趋势做告警，就需要对曲线的趋势进行拟合。这里使用EWMA算法计算原始窗口的平均值，有了平均值之后可以计算方差，方差乘以一定的倍数可以得出对于振幅的容忍范围。比较实际的值是否超出了这个范围就可以知道是否可以告警了。超出了上界，可能是突然用户量突然激增了。超出了下界，可能是营销活动结束了，用户快速离开，也可能是光纤断了，玩家掉线了。<br>
>实际使用中发现这种基于曲线平滑度的算法的优点有:
* 依赖的数据少，只需要近期的历史，不依赖于周期性
* 非常敏感，历史如果波动很小，方差就很小，容忍的波动范围也会非常小
>缺点也是显著的:
* 过于敏感，容易误报。因为方差会随着异常点的引入而变大，所以很难使用连续三点才告警这样的策略
* 业务曲线可能自身有规律性的陡增和陡降

### absolute_periodicity_min

>这是一种利用时间周期性的最简单的算法,很多监控曲线都有这样以一天为周期的周期性（早上4点最低，晚上11点最高之类的）。
使用min(14 days history) * 0.6作为下界。例如：对于12:05分，有14天对应的点，取最小值。对于12:06分，有14天对应的点，取最小值。这样可以得出一条一天的曲线。然后对这个曲线整体乘以0.6。  <br>
>这其实是一种静态阈值告警的升级版，动态阈值告警。实际使用中0.6当然还是要酌情调整的。而且一个严重的问题是如果14天历史中有停机发布或者故障，那么最小值会受到影响。也就是说不能把历史当成正常，而是要把历史剔除掉异常值之后再进行计算。一个务实的近似的做法是取第二小的值。 <br>
### absolute_periodicity_max
>absolute_periodicity_min算法对应过滤最大值的算法

### amplitude_periodicity
>有些时候曲线是有周期性，但是两个周期的曲线相叠加是不重合的。比如两个周期的曲线一叠加，一个会比另外一个高出一头。对于这种情况，利用绝对值告警就会有问题。
比如今天是10.1日，放假第一天。过去14天的历史曲线必然会比今天的曲线低很多。那么今天出了一个小故障，曲线下跌了，相对于过去14天的曲线仍然是高很多的。这样的故障如何能够检测得出来？一个直觉的说法是，两个曲线虽然不一样高，但是“长得差不多”。那么怎么利用这种“长得差不多”呢？那就是振幅了。 <br>
>与其用x(t)的值，不如用x(t) – x(t-1)的值，也就是把绝对值变成变化速度。可以直接利用这个速度值，也可以是 x(t) – x(t-1) 再除以 x(t-1)，也就是一个速度相对于绝对值的比率。比如t时刻的在线900人，t-1时刻的在线是1000人，那么可以计算出掉线人数是10%。这个掉线比率在历史同时刻是高还是低？那么就和前面一样处理了。 <br>
>实际使用中有两个技巧：可以是x(t) – x(t-1），也可以是x(t) – x(t-5）等值。跨度越大，越可以检测出一些缓慢下降的情况。
另外一个技巧是可以计算x(t) -x(t-2)，以及x(t+1) – x(t-1)，如果两个值都异常则认为是真的异常，可以避免一个点的数据缺陷问题。<br>
>优点：
* 比绝对值要敏感
* 利用了时间周期性，规避了业务曲线自身的周期性陡降
>缺点：
* 要求原曲线是光滑的
* 周期性陡降的时间点必须重合，否则误警
* 按百分比计算容易在低峰时期误警
* 陡降不一定代表故障，由上层服务波动引起的冲高再回落的情况时有发生

### recent_compare
>们可以使用最近时间窗口（T）内的数据遵循某种趋势,比如我们将T设置为7，则我们取检测值（nowvalue）和过去7个（记为i）点进行比较，如果大于阈值我们将count加1，如果count超过我们设置的countnum，则认为该点是异常点。 <br>
>360的lvs流量异常检测的阈值设置方法。通常阈值设置方法会参考过去一段时间内的均值、最大值以及最小值，我们也同样应用此方法。取过去一段时间（比如T窗口）的平均值、最大值以及最小值，然后取max−avg和avg−min的最小值。即threshold = min(max-avg, avg-min)，之所以取最小值的原因是让筛选条件设置的宽松一些，让更多的值通过此条件，减少一些漏报的事件。 <br>




