import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
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
        msg.attach(zipAttach)

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(login, password)  # 登录SMTP服务器
        server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
        server.quit()  # 断开连接
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送邮件失败：{e}")


def senfEmail(title,contentFilepath):
    if title == "":
        title = '测试邮件'
    if contentFilepath == "":
        content = '这是一封测试邮件'
        attach = None
    else:
        with open('path_to_your_file.zip', 'rb') as f:
            attach = MIMEApplication(f.read(),_subtype="zip")
            attach.add_header('Content-Disposition','attachment',filename='file_name.zip')
            #msg.attach(attach)
    send_email(sender_email, receiver_email, title, content, smtp_server, smtp_port, login, password,attach)
