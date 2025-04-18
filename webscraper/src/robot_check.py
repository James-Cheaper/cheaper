from urllib.robotparser import RobotFileParser

class RoboCheck:
    def __init__(self,base_url,user_agent):
        self.robot_parser = RobotFileParser(f"{base_url}/robots.txt")
        self.robot_parser.read()
        self.user_agent = user_agent

    def can_fetch(self, path="/") -> bool:
        #check if all clear to parse a specific url path
        return self.robot_parser.can_fetch(self.user_agent, path)