# 提取一阶逻辑表达式，参数为文件名，返回回答
import PyPDF2
from call_api import askChatGPT


def getExpress(fileName):
    # 打开PDF文件并读取文本
    pdf_file = open(fileName, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    prompt = "请阅读文本a:{} \n请你按文本中的逻辑关系进行组合生成一阶逻辑表达式。用于判断是否患病\
             一个一阶阶逻辑表达式例子是[(A(x) ∧ B(x) ∧ C(x)) ∧ (D(x) ∨ E(x) ∨ F(x) ∨ G(x) ∨ H(x) ∨ I(x) ∨ J(x))] → P(x)\
             或(SystolicBP(x) ≥ 140 ∧ DiastolicBP(x) ≥ 90) ∧ NotOnSameDay(x) ∧ RepeatThreeTimes(x) → Diagnosis(x)。\
                请按照上面方法尝试给出文本a的一阶逻辑表达式，并进行解释。我十分在意逻辑的正确性。".format(text)
                               
    message = askChatGPT(prompt)
    return message

def getLogic(path):
    prompt = "请阅读文本:"+path+"\n请你先识别出文本里的重要名词，再按文本中的逻辑关系进行组合最后生成出一阶逻辑表达式。一阶逻辑表达式例子是[(A(x) ∧ B(x) ∧ C(x)) ∧ (D(x) ∨ E(x) ∨ F(x) ∨ G(x) ∨ H(x) ∨ I(x) ∨ J(x))] → P(x)或(SystolicBP(x) ≥ 140 ∧ DiastolicBP(x) ≥ 90) ∧ NotOnSameDay(x) ∧ RepeatThreeTimes(x) → Diagnosis(x)。请用一条或多条一阶逻辑来表达以上的知识，即给出可以诊断是否患新冠肺炎的一阶逻辑表达式，并且给出表达式符号的意义。我十分在意逻辑的正确性。"
    answer = askChatGPT(prompt)
    return answer
# prompt2 = "请将上述一阶逻辑表达式和相关文字描述分开来"
# askChatGPT(prompt)

# TEST1：读取PDF文件
# prompt = "请阅读文本:{text} \n请你先识别出文本里的重要名词，再按文本中的逻辑关系进行组合最后生成出一阶逻辑表达式。一阶逻辑表达式例子是[(A(x) ∧ B(x) ∧ C(x)) ∧ (D(x) ∨ E(x) ∨ F(x) ∨ G(x) ∨ H(x) ∨ I(x) ∨ J(x))] → P(x)或(SystolicBP(x) ≥ 140 ∧ DiastolicBP(x) ≥ 90) ∧ NotOnSameDay(x) ∧ RepeatThreeTimes(x) → Diagnosis(x)。请用一条或多条一阶逻辑来表达以上的知识，即给出可以诊断是否患高血压疾病的一阶逻辑表达式。我十分在意逻辑的正确性。"
# 回答：
# 文本：如果一个人的收缩压（SystolicBP）大于140毫米汞柱（mmHg），舒张压（DiastolicBP）大于90 mmHg，且三次测量的结果不是在同一
# 天取得，那么他很可能患上高血压疾病。

# 重要名词：SystolicBP，DiastolicBP，SameDay，RepeatThreeTimes，Diagnosis

# 一阶逻辑表达式：[(SystolicBP(x) ≥ 140 ∧ DiastolicBP(x) ≥ 90) ∧ NotOnSameDay(x) ∧ RepeatThreeTimes(x)] → Diagnosis(x)


# TEST2：
# prompt = "你是一名肺炎医生，作为医生，疾病诊断需要有较高的准确性，请自行搜索并整合出官方可信任渠道提供的肺炎诊断医疗指南，根据整合出的肺炎诊断标准，先识别出与肺炎相关的重要名词，再按文本中的逻辑关系进行组合最后生成出一阶逻辑表达式（使用谓词和逻辑联结词）。请用一条或多条一阶逻辑来表达以上的知识，即给出能诊断是否患肺炎的数学符号化一阶逻辑表达式，我十分在意逻辑的正确性。"
# 回答：
# 肺炎诊断条件：

# (1) 出现发热、咳嗽、气促、乏力等症状，且
# (2) 支气管炎片检查或者实验室检查（如血液检查、胸部CT扫描等）结果显示有肺炎相关的改变

# 一阶逻辑表达式：

# 肺炎诊断条件：(发热 ∧ 咳嗽 ∧ 气促 ∧ 乏力) ∧ (支气管炎片检查 ∨ 血液检查 ∨ 胸部CT扫描)
