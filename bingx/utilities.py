import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def convert_date_to_epoch_ms(time):
    pass


def get_system_time():
    return str(int(time.time() * 1000))

def get_random_agent():
    software_names = [SoftwareName.CHROME.value, SoftwareName.SAFARI.value, SoftwareName.FIREFOX.value, SoftwareName.OPERA.value, SoftwareName.EDGE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value, OperatingSystem.ANDROID.value, OperatingSystem.IOS.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()


print(get_random_agent())