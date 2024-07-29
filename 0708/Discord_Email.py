import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
# 使用示例
sender_email = "1073138529@qq.com"
receiver_email = "1073138529@qq.com"
subject = "测试邮件"
body = "这是一封测试邮件。"
smtp_server = "smtp.qq.com"
smtp_port = 465
login = "1073138529@qq.com"
password = "wnkokurwrcktbeab"

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password,zipAttach):
    # 创建MIMEMultipart对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    if zipAttach == None:
        print("NO ZIP")
    else:
        print("ATTACH")
        msg.attach(zipAttach)

    try:
        print("TRY")
        # 连接到SMTP服务器
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(login, password)  # 登录SMTP服务器
        server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
        server.quit()  # 断开连接
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送邮件失败：{e}")


def senfEmail(title,contentFilepath):
    content = "'这是一封测试邮件'"
    if title == "":
        title = '测试邮件'
    if contentFilepath == "":
        content = '这是一封测试邮件'
        attach = None
    else:
        with open(contentFilepath, 'rb') as file:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(file.read())
            
            encoders.encode_base64(part)
            
            part.add_header('Content-Disposition', f"attachment; filename= {contentFilepath.split('/')[-1]}")
            #msg.attach(attach)
    send_email(sender_email, receiver_email, title, content, smtp_server, smtp_port, login, password,part)


#path = 'E:/hero/email/shangyang/Images_test/Videos\combine.mkv'
#senfEmail("123",path)