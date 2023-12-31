from call_api import askChatGPT

# 根据症状给出诊断结果


def diagnosis(content):
    return askChatGPT("你是一名专业的医生，作为医生，疾病诊断需要有较高的专业性，准确性和科学性，现在有一名患者找你看病，\
           根据整合出的疾病诊断标准以及患者的症状描述，结合患者年龄，性别，给出诊断结果\
           以下是患者的症状描述：" + content + " 请给出一定可靠的诊断结果。")

# 根据症状给出治疗建议


def suggest(content):
    return askChatGPT("你是一名专业的医生，作为医生，治疗建议需要有较高的专业性，准确性和科学性，现在有一名患者找你看病，\
           根据整合出的资料以及患者的症状描述，结合患者年龄，性别，给出治疗建议\
           以下是患者的症状描述：" + content + " 请给出治疗建议。")
