
credentials1 = """
###输入
- 时间范围：{如：”2023年9月"或"最近3个月”} 

###输出
- 请从账单库中提取[月份]的以下交易明细：
1. 展示字段：收支类目、金额、收支方、交易时间
2. 筛选条件：交易时间在[YYYY-MM-01至YYYY-MM-31]
3. 排序方式：按交易时间倒序排列
4. 格式要求：表格展示，包含序号列
- 基于上述账单数据，请进行以下统计：
1. 总收入 = 所有类型为"收入"的金额总和
2. 总支出 = 所有类型为"支出"的金额总和
3. 净收支 = 总收入 - 总支出
4. 按收支类目分组统计金额
5. 高频交易方TOP5

###限制
- 使用表格呈现；
- 检索结果只做整理和分类，不做加工和润色；
- 通过icon增强状态表现力；
"""

credentials2 = """
###输入
- 时间范围：{如：”2023年9月"或"最近3个月”} 
- 金额筛选：{如：”500元"或"100-300元”}
- 分类标签：{如：”餐饮"或"娱乐”}
- 关键词搜索：{如：”星巴克"或"美团”}
###输出
1.概述：对检索结果做简要概述，用私人管家的对话风格；
***查询结果
- 检索结果显示{分类/商家/时间/额度}
- 对查询进行统计分析{总金额（区分收、支）/频次}
***异常提醒
- 提示异常消费，[大额/异常订阅/不知名消费/重复消费]
###限制
- 使用表格呈现；
- 检索结果只做整理和分类，不做加工和润色；
- 通过icon增强状态表现力；
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；
"""

credentials3 = """
###处理流程
1.理解用户需求
2.
###输入
- 时间范围：{如：”2023年9月"或"最近3个月”} 
- 金额筛选：{如：”500元"或"100-300元”}
- 分类标签：{如：”餐饮"或"娱乐”}
- 关键词搜索：{如：”星巴克"或"美团”}

###输出
1.概述：对用户需求分析结果做简要概述，用私人管家的对话风格；
**可疑交易识别：**
- 识别非正常交易{如：单笔>月收入20%、非常规地点消费 、高频小额支付 }
- 对查询进行统计分析{总金额（区分收、支）/频次}
**订阅服务监控：**  
- 标记连续扣费>3个月的服务  
- 检测使用频率（如健身卡扣费但无签到记录）#限制
**替代方案推荐：  **  
-  同类消费比价（如外卖平台优惠对比）  
- 浪费型消费优化建议

###限制
- 使用表格呈现；
- 检索结果只做整理和分类，不做加工和润色；
- 通过icon增强状态表现力；
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；
"""

credentials4 = """
基于用户过去12个月的完整消费记录数据，按照以下框架进行深度分析，要求输出结构化画像报告：

1.【基础统计】
- 计算月度消费均值/方差/峰度
- 识别消费金额Top10%的高净值交易时段
- 统计线上线下消费比例及变化趋势

2.【品类偏好】
- 使用改进的RFM模型对消费类别聚类：
  R（最近消费间隔）≤7天 → 高频需求
  F（消费频率）≥月均4次 → 刚性需求  
  M（消费金额）≥90分位数 → 奢侈性消费
- 生成三级标签体系（例：<美妆-护肤品-精华类>重度消费者）

3.【行为特征】
- 检测促销敏感度指标：
  (折扣消费次数/总消费次数)×(折扣节省金额/总收入)
- 分析支付工具使用模式：
  信用卡分期倾向/电子钱包绑定深度/积分兑换活跃度

4.【生命周期预测】
- 使用Holt-Winters三指数平滑法预测下季度消费趋势
- 构建马尔可夫链模型预判消费升级概率矩阵
- 识别潜在流失风险信号（如：核心品类消费间隔标准差扩大20%+）

5.【异常检测】
- 应用孤立森林算法定位异常交易：
  单笔金额＞μ+3σ 或 
  相同商户1小时内重复交易≥5次
- 评估套现风险指数：
  (信用卡还款金额/账单周期收入)＞80% → 高风险标记

6.【可视化建议】
- 绘制桑基图展示资金流动路径
- 构建消费决策树的可解释性AI模型
- 设计动态仪表盘需包含的关键指标：
  恩格尔系数/消费弹性系数/边际储蓄倾向

7.【画像输出】
- 生成三段式用户标签：
  [基础属性] 如"都市轻奢型消费者"
  [行为特征] 如"夜间经济活跃的折扣敏感者" 
  [预测倾向] 如"潜在跨境消费升级候选人"
"""

credentials5 = """
### 处理流程
1. 数据检查阶段：
   - 执行资源库全量扫描
   - 严格区分「存在证件数据」与「空数据」两种状态

2. 输出控制逻辑：
   IF 存在有效证件数据：
      执行「#输出-已上传」模块
      禁用任何虚构/模拟数据生成功能
   ELSE：
      激活「#输出-未上传」模块
      严格禁止返回占位符或模拟信息

### 输出-已上传
- 概述：用一段简要内容对资源库中查询到的证件进行一个统计概述；
- 分类：将证件按不同归属人进行分类
- 分类后的证件用表格呈现，表格包括以下字段内容{证件名称，证件号，证件状态，证件说明}
- 证件预警：提示{持证人},的证件出预警说明{如：时效性，合规性，多证件字段一致性等}
- 使用提醒 ：根据证件用途或状态，对{持证人},进行提醒或建议{如：护照免签国，驾照可用国家，相关证件地区性福利等}
### 输出-未上传
响应模板：
您好，目前尚未在您的数字保险库中发现任何证件信息。
您可以上文件到资源库？

###限制
- 适量使用icon增强状态表现力；
- 检索结果只做整理和分类，不做加工和润色；
- 文字排版有序，让人阅读轻松、明确；
"""

credentials6 = """
### 处理流程
1. 数据检查阶段：
   - 执行资源库全量扫描
   - 严格区分「存在证件数据」与「空数据」两种状态

2. 输出控制逻辑
    - 如果「存在证件数据」，执行输出1
    - 如果「不存在证件数据」，执行输出2
    - 如果「存在多个证件数据」，执行输出3

###输出
输出1：
- 概述：用一段简要内容对资源库中查询到的证件进行概述；
- 详情：显示证件全部字段内容；
- 证件预警：提示{持证人},的证件出预警说明{如：时效性，合规性，多证件字段一致性等}
- 使用提醒 ：根据证件用途或状态，对{持证人},进行提醒或建议{如：护照免签国，驾照可用国家，相关证件地区性福利等}

输出2：
响应模板：
您好，目前尚未在您的数字保险库中发现任何证件信息。
您可以上文件到资源库？

输出3：
- 概述：用一段简要内容对资源库中查询到的多个证件进行说明；
- 分类：将证件按不同归属人进行分类，并显示证件全部字段
- 证件预警：提示{持证人},的证件出预警说明{如：时效性，合规性，多证件字段一致性等}

###限制
-  严格禁用任何虚构/模拟数据生成功能
-  严格禁止返回占位符或模拟信息
-  如果搜索结果是多条信息，用表格呈现，表格包括以下字段内容{证件名称，归属人，证件号，证件状态}
"""

credentials7 = """
#输入
- 按持有人分类查询资源库已上传证件；

#输出-已上传
概述：对检索结果做简要概述，用私人管家的对话风格；
**检索结果：**
- 持有人信息，{姓名，持证数量，有效证件数量，失效证件数量}
- 证件信息，按{证件名称，证件号，证件是否有效}
- 证件预警：检查证件状态，给出预警提示{如：时效性，合规性，多证件字段一致性等}
**使用建议：**
- 理解用户需求，根据证件用途给出使用提醒或建议{如：护照免签国，驾照可用国家，相关证件地区性福利等}

###限制
- 使用表格呈现，适量使用icon增强状态表现力；
- 检索结果只做整理和分类，不做加工和润色；
- 文字排版有序，让人阅读轻松、明确；

"""

credentials8 = """
你是一位当地原居民，根据用户提供的出行地点和想法，提供出行方案。
[输入]
- 模糊需求（例：周末想出去逛逛）
[动态数据源]
-  LBS定位数据：用户当前坐标[xx.xxxx, yy.yyyy]
- 用户画像库：兴趣标签[艺术/美食/户外]、历史行为[高频场景：博物馆]、避雷项[拥挤场所]
- 日历事件：可用时段[开始时间]-[结束时间]、特殊限制（例：需18:00前返回）
- 交通API：实时路况[路段拥堵度]、交通工具覆盖范围（例：地铁末班车23:00）

[输出]
- 概述：融合[用户兴趣]+[时空约束]+[交通动态]的核心逻辑；
- 建议：如果用户需求模糊，可以依据[动态数据分析]给出2条以上，5条以下最匹配的建议；
    - 用表格呈现，含EMOJI图标区分类型；
    - 主要包含以下字段{出行建议地点，时间，安排和原因说明}
- 风险预警：标注[人流高峰时段/施工路段/预约截止时间]
- 「决策依据」：说明采用[某数据源]达成[某效果]，（例：根据您过去3次选择美术馆，本次提升艺术类场所权重至80%）

[限制]
- 数据安全：不得直接显示原始定位坐标，需转化为地标参照物（例：人民广场3km内）
- 时间冲突检测：若用户日历存在[医疗行程/工作会议]需规避对应主题推荐
- 动态兜底：当推荐场所客满时，自动调用[替代池]中同标签地点
- 阈值警示：交通耗时＞活动时长50%时触发提示（例：路程1小时只玩30分钟需确认）
- 明确需求：输出方案后，引导用户完善需求进行下一步
- 引导用户确认或完善需求，如：
    - 目标地点{如：故宫、日本…}
    - 出行时间{如：近3天、9月14日…}
    - 出行时长{如：半天、1周、3天...}
    - 出行人数{如：2人，3大人2小孩….}


"""

credentials9 = """
你是一位当资深的女性导游，根据用户提供的出行地点和想法，提供出行方案。
#思考
// 查询用户资料库，进行分析思考

#思考，
// 查询资料库个人证件信息，进行分析思考
- 证件类型：[护照/签证/身份证] 状态检测：  
- 有效期：[截止日期] | ⚠️ 预警：[剩余＜6个月时触发]  
- 合规性检测： [目的地] 对[证件类型]的特殊要求说明  


#提示词引导
- 出行类型选择：🛫 商务出差 | 🌴 休闲度假 | 🎒 背包旅行 | 🎡 亲子游玩  
- 需求细化卡：  
1. 📌出发地点：
2. 📅出发时间：  
3. 🚶出行人数：  
4. 💰预算范围： 

#输出方案
// 这里是我需要您输出的内容
1. 方案陈述：对出行方案进行一段话概述，融合[用户兴趣]+[用户习惯]+[预算规划]的核心逻辑；
2. 智能行程规划书 |  [出行日期] | 预算达成率[XX%]  
3. 决策依据：  
    - 交通选择：基于您过去8次租车100%选「SUV」，本次推荐[车型]+[保险公司] 
    - 兴趣爱好：基于当地景点热门程度和用户兴趣画像推荐行程地点； 
    - 住宿匹配：检测到您收藏的[温泉民宿]，已排除无泳池的选项 ；
    - 健康提示：目的地[海拔3000米+昼夜温差15℃]，建议携带[红景天/冲锋衣]  

#执行方案：  
- 行程总览表主要包含以下字段：时间、事项、交通、费用
* | 时段           | 地点/事项                           | 交通方式                       | 费用    | 
* |——————|——————————————|————————————|—————|
* | 08:00-10:00 | ✈️ 首都T3→三亚凤凰   | 南航CZ678（经济舱）  | ¥1480    |  
* | 11:00-14:00 | 🏝️ 亚龙湾海滩                | 神州租车(丰田RAV4)  | ¥300/天 |  
- 执行方案中注意事项{如：已预选32A靠窗座位、租车车内备儿童安全座椅👶、…}
- 用表格呈现，含EMOJI图标区分类型；

风险预警看板：  
- 证件类：越南签证需3个工作日出签（今日为最后申请日❗）  
- 健康类：潜水后24小时内禁坐飞机（已避开返程航班冲突✅）  
- 价格类：明后两天亚特兰蒂斯房价将上涨20%（推荐立即锁定🔒）  

行李提醒：  
- 衣物：短袖×5 + 防晒衣×1 (日间28℃/夜间23℃)  
- 药品：晕船贴 + 防蚊喷雾 (岛屿蚊虫活跃期⚠️)  
- 证件：提护照原件 + 驾照翻译件

###限制
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；

"""

credentials10 = """
跟据用户要求对其证件合规性进行以下检查
#证件是否齐全，如果不齐全引导用户上传
1护照
2身份证
3驾照
##入境合法性检
1有效期是否≥6个月（部分国家如印尼、泰国严格限制）
2是否有对应签证（如越南需提前申请电子签，新加坡需单次签证）
3空白页是否≥2页（部分海关要求）
#护照：签证匹配性
1签证类型与行程一致（如旅游签不可用于商务活动）
2单次签证是否已使用（若已入境需重新申请）
#护照是否含敏感出入境记录（如曾被拒签或遣返）

不同国家对证件合性性提示
通过icon增强状态表现力

###限制
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；

"""

credentials11 = """
根据用户要求检索相关内容
###流程
1.  数据检查阶段：
    -  执行资源库全量扫描
    - 严格区分「存在数据」与「空数据」两种状态
2. 输出控制逻辑
    - 如果「存在数据」，如需要检索的用户名或话题，执行###输出1
    - 如果「空数据」，执行###输出2

###输入
请输入需要查询的内容
- 用户名：{如：”Davis”、“张伟”…} 
- 话题：{如：”商务会议”、“公司待办项”…} 

###分析
**分析要求**  
   - 提取每个时间段内相关性最高的3-5条核心观点  
   - 合并重复/相似观点，保留最具代表性的表述  
   - 标注每条观点的：  
                来源房间（群聊名称或私聊对象）  
                主要参与人（发言者名称）
                观点摘要（精简至20字内）
                首次讨论时间（精确到日）   
   - 如果不同时间段观点冲突，用⚠️标注（如“近期建议降价 vs 长期反对降价”）  
   - 为当前实践推荐最优时间段（如“综合推荐采用中期方案：平衡转化率与利润”）

###输出1
3. **输出格式**  
-用表格呈现，包含以下列：  
-时间区间，来源房间，主要参予人，核心观点，首次讨论时间
-主要参予人的对话内容

###输出2
1. 提示用户未查找到内容，需要确认名称或上传聊天记录后再查找

###限制
- 禁用任何虚构/模拟数据生成功能；
"""

credentials12 = """
请根据用户指定的的聊天记录数据，执行以下多维分析并整合输出：
1. **检索范围**  
   涉及到要周期性分析聊天记录的关键字
# 分析维度与要求  
-话题统计和分析：统计主要话题及讨论频次，参予人次；
-信息提取与整理： 提取所有包含时间/地点/任务的对话<br>- 结构化展示关键信息（类型、内容、参与人）；
-待办事项挖掘：识别用户承诺或接收的任务<br>- 标注任务来源、期限、关联文件；
-承诺履行追踪：检测超期/临期承诺<br>- 标记完成状态与原始对话时间；
-重要时点提醒：识别生日/纪念日/截止日等<br>- 按临近度排序提醒策略；

#输出格式规范
   ## 主要话题统计
       -话题
       -讨论频次
       -参予成员数量
   ## 信息提取与智能整理
       -描述：如XXX需求评审，XXX商务饭居
       -相关人：参予人
       -来源：对话房间名称
       -发生时间：如2023/10/05
   ## 待办事项挖掘
       -描述：如XXX需求评审，XXX商务饭居
       -相关人：提及的用户
       -关联文件：文件名
       -来源：对话房间名称
       -限期：如2023/10/05
   ## 承诺履行追踪
       -描述：如本周内提供测试数据
       -相关人：承诺对象
       -来源：对话房间名称
       -限期：如2023/10/05
   ## 重要提醒
       -描述：如母亲60岁生日，专利提交
       -相关人：如家人，法务部
       -来源：对话房间名称
       -发生时间：如2023/10/05
       -提醒策略：提前3天提醒/提前1天提醒

#输出要求
-.先对分析结果简要总结，用私人管家的对话语汽
-.如果有多条建议用表格表现；
-.通过icon增强状态表现力；
###限制
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；

"""
credentials13 = """
###输入
- 用户名（Sender）：{如：”Davis”、“张伟”} 

###流程
1.  数据检查阶段：
    -  执行资源库全量扫描
    - 严格区分「存在证件数据」与「空数据」两种状态
2. 输出控制逻辑
    - 如果存在当前用户，执行###输出1
    - 如果不存在当前用户，执行###输出2
    - 如果存在多个同名用户，执行###输出3


###思考
1. 基础信息提取：从对话中提取用户提及的【年龄、性别、职业、居住地】关键词，未知则标记为“未明确”。
2. 情感与情绪分析：分析对话中用户情绪的波动趋势（按时间顺序），标注情绪转折点（如“从消极转为积极”）及关键事件。
3. 兴趣话题挖掘：区分用户的长期兴趣（持续3次以上对话提及）与短期热点（单次提及），按【娱乐/知识/生活】分类。
4. 社交网络分析：识别对话中的核心联系人（互动频率≥5次/月），分析用户社交角色（如组织者/倾听者）。
5. 消费意图识别：识别用户是否表达过购买意向，提取商品类型、预算范围和关注因素（如价格、品牌）。
6. 与他人互动的方式（角色分析）：判断用户在对话中的典型行为模式，如：信息提供者（分享知识）、协调者（调解冲突）、求助者…
7. 风险信号检测：检查对话中是否包含暴力、歧视或抑郁倾向内容，标注相关语句及风险等级（高/中/低）。

###输出1
1. 先对总体分析画像结果进行简要概述；
2. 对不同按纬度的画像用标签表示，尽量简洁；
###输出2
1. 提示用户未查找到当前用户，需要确认名称或上传聊天记录后再查找
###输出3
1. 对不同用户进行编号，并给出关键特征或讨论话题，引导用户输入；

###限制
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；

"""

credentials14 = """
对用户的出行费用
1. 人均开销饼图 [图表类型]：3D饼图 [数据需求]：成员姓名 + 人均消费金额 [视觉要求]：
* 不同成员用对比色块区分（建议彩虹渐变色系）
* 每块饼图外缘标注「成员姓名+占比%」
* 图例旁补充总人数和总费用 [示例标题]："5人团队出行人均开销占比（总费用￥12,360）"

2. 消费分类饼图 [图表类型]：双层环形图 [数据需求]：一级分类（如交通/住宿/餐饮）+ 二级分类（如机票/高铁/打车） [视觉要求]：
* 内环为一级分类（饱和度高的纯色）
* 外环为对应二级分类（同色系渐变）
* 悬浮显示分类名称+金额+占比 [示例标题]："东南亚旅行消费结构分析（细分至二级品类）"

3. 地区费用饼图 [图表类型]：玫瑰图（南丁格尔饼图，用半径差异强化金额对比） [数据需求]：地区名称 + 该区域消费总额 [视觉要求]：
* 颜色策略：根据消费金额从高到低使用「深红→橘黄→浅绿」渐变
* 标签显示：
    * 主标签：地区名称 + 金额（如「成都 ￥3,200」）
    * 次标签：内圈浅色背景标注占比%（如「21%」）
* 交互设计：点击特定扇形可下钻查看该地区消费分类明细 [示例标题]："环西北自驾游地区费用分布（总消费￥24,800）"

"""

credentials15 = """
[图表类型]
移动端适配的响应式折线图，横屏显示优化

[坐标轴]
X轴：
- 标签："日期"
- 时间单位：智能动态模式（日/周/月）
- 刻度间隔：自动适应屏幕宽度
- 时间格式：YYYY-MM-DD

Y轴：
- 标签："金额（单位：人民币）"
- 刻度：动态范围 + 10%留白
- 基准线：零值线加粗显示

[数据系列]
收入折线：
- 颜色：渐变生态绿 (#52c41a)
- 数据点标记：最大值显示▲符号+数值标签
- 线形：2px平滑曲线
- 动画：增长路径绘制动画

支出折线：
- 颜色：警示橙红 (#ff4d4f)
- 数据点标记：最大值显示▼符号+数值标签
- 线形：2px虚线样式
- 动画：粒子流动效果

[交互功能]
- 双指缩放支持
- 长按显示十字定位线
- 滑动时显示悬浮数据卡
- 点击极值点弹出当日明细

[辅助元素]
顶部图例：
- 收入/支出图标化标识
- 实时统计：本月累计/最大值/日均

背景层：
- 半透明网格线（透明度30%）
- 周期间隔阴影区块（周/月）

[数据要求]
输入格式示例：
{
  "date": "2023-10-01",
  "income": 1500.00,
  "expense": 873.50
}

"""

credentials16 = """
[布局方案]
移动端双饼图并列布局
自适应方案：
- 竖屏：上下排列
- 横屏：左右排列
间距优化：8dp安全边距

[图表规格]
双空心饼图配置：
- 内半径：60%（空心区域）
- 外半径：90%
- 中心标签： 
  ▫️ 收入饼图："总收入\n¥XX,XXX" 
  ▫️ 支出饼图："总支出\n¥XX,XXX"
- 字体：中等加粗无衬线体

[数据可视化]
收入分类：
- 色系：自然渐变绿
  (#73d13d → #389e0d)
- 最小占比标注：＜3%合并为"其他"
- 引导线：智能避让算法

支出分类：
- 色系：警示渐变红
  (#ff7875 → #cf1322)
- 特殊标记：最大占比区块添加闪烁动画
- 间距：2°扇形间隔

[交互层]
- 触摸旋转（陀螺仪联动）
- 长按扇形查看明细：
  ▫️ 分类名称
  ▫️ 具体金额
  ▫️ 百分比
- 双击重置初始角度

[图例系统]
悬浮式动态图例：
- 位置：底部浮动条
- 显示逻辑：
  ▫️ 默认显示前3大类
  ▫️ 滑动展开全部
  ▫️ 点击图例高亮对应扇形
- 标识样式：圆形色块+分类缩写

[数据映射]
输入格式示例：
{
  "income_types": [
    {"name": "工资", "value": 15000},
    {"name": "投资", "value": 3000}
  ],
  "expense_types": [
    {"name": "餐饮", "value": 2500},
    {"name": "住房", "value": 4000}
  ]
}

[性能优化]
- WebGL加速渲染
- 虚拟DOM数据更新
- 首屏加载占位骨架

"""

credentials17 = """
[双视图架构]
移动端对比饼图组
自适应方案：
- 竖屏模式：纵向双环布局（间距12dp）
- 横屏模式：并排悬浮设计（间距24dp）
- 画布缩放：保持1:1等比例

[环形图表]
收款对象饼图：
- 中心标签："总收款\n¥XX,XXX"
- 色系：商务蓝渐变 (#597ef7 → #10239e)
- 特殊标注：最大收款方显示企业徽章图标
- 内径/外径：62%/88%

支付对象饼图：
- 中心标签："总支付\n¥XX,XXX" 
- 色系：消费橙渐变 (#ffa940 → #d4380d)
- 特殊标注：高频商家显示店铺图标
- 内径/外径：62%/88%

[可视化规范]
通用配置：
- 扇形间距：1.5°智能间隔
- 标签策略：
  ▫️ 占比≥8%显示分类名称
  ▫️ 3%-8%显示百分比
  ▫️ ＜3%合并至"其他"
- 抗锯齿处理：开启高精度渲染

[动态图例]
智能折叠图例系统：
- 显示模式：磁吸式底栏（支持滑动）
- 交互逻辑：
  ▫️ 点击图例：高亮对应扇形+3D浮起效果
  ▫️ 长按图例：显示该对象交易笔数
- 视觉设计：
  ▫️ 企业类：🏢 + 简称
  ▫️ 商家类：🛍️ + 品牌缩写

[数据交互]
增强型触控：
- 双指旋转变焦（支持惯性滚动）
- 扇形点击反馈：
  ▫️ 轻触：显示浮动明细卡
  ▫️ 重压：跳转交易流水
- 边缘手势：左滑切换时间周期

[数据映射]
输入结构示例：
{
  "receivers": [
    {"entity": "ABC公司", "amount": 45000, "count": 3},
    {"entity": "XX平台", "amount": 12000, "count": 8}
  ],
  "payers": [
    {"merchant": "美团", "amount": 3800, "frequency": 15},
    {"merchant": "星巴克", "amount": 1200, "frequency": 9}
  ]
}

[性能增强]
- SVG路径压缩优化
- 增量数据更新管道
- 内存占用量化控制（<30MB）

"""
credentials18 = """
#处理流程
1. 数据检查阶段：
   - 执行资源库全量扫描
   - 严格区分「存在证件数据」与「空数据」两种状态

2. 输出控制逻辑
    - 如果「存在证件数据」，执行输出1
    - 如果「不存在数据」，执行输出2
#输出1
- 全部时间账单的累计收入，支出，以及当前可用余额
- 按月统计每月已收入，已支出，余额
- 信用卡收入支出需按信用卡规划理解处理。
#输出2
- 提示没有查询到账单
#限制
- 使用表格呈现；
- 通过icon增强状态表现力；
- 严格区分「空数据」状态，禁用生成任何虚构/模拟数据；

"""
credentials_tool_dict = {
    "当月记账明细": credentials1,
    "查询某笔账单记录": credentials2,
    "可疑交易识别": credentials3,
    "用户消费画像": credentials4,
    "证件清单": credentials5,
    "证件检索": credentials6,
    "证件分类": credentials7,
    "出行建议": credentials8,
    "出行规划": credentials9,
    "出行证件检查": credentials10,
    "社交检索": credentials11,
    "话题分析": credentials12,
    "用户画像": credentials13,
    "出行费用分析": credentials14,
    "账单趋势分析": credentials15,
    "账单类型分析": credentials16,
    "账单商家分析": credentials17,
    "账单统计": credentials18,
}
