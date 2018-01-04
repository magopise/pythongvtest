from rasa_core.channels.rest import HttpInputChannel
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.facebook import FacebookInput
from rasa_core.channels.custom import CustomInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from botlerchannel import SimpleWebBot
# load your trained agent

agent = Agent.load("models/dialouge", interpreter=RasaNLUInterpreter("models/default/current", "nlu_model_config.json"))
input_channel = SimpleWebBot()
agent.handle_channel(HttpInputChannel(5050, "/app", input_channel))
