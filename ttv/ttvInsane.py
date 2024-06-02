from twitchio.ext import commands
import obswebsocket, time
from obswebsocket import obsws, requests

class Bot(commands.Bot):

    cntFormanInsane = 0
    ttv_token = "TOKEN"
    ttv_channel = "CHANNEL"
    ttv_message = "MESSAGE AFTER TRIGGER"
    ttv_trigger = "MESSAGE THAT TRIGGER THE SOURCE"
    obs_scene_name = "SCENE NAME"
    obs_source_itemId = OBS_SOURCE_ITEM_ID
    ws_host = "IP"
    ws_port = PORT
    ws_pass = "PASS"

    ws = None

    def __init__(self):
        super().__init__(token=self.ttv_token, prefix='!', initial_channels=[self.ttv_channel])

        # Set up OBS WebSocket connection
        self.ws = obsws(self.ws_host, self.ws_port, self.ws_pass)
        self.ws.connect()

    async def event_ready(self):
        print(f'[+] Logged in as | {self.nick}')
        print(f'[+] User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)

        if message.content == self.ttv_trigger:
            self.cntFormanInsane += 1
            print(self.cntFormanInsane)
            if self.cntFormanInsane >= 5:
                await self.switch_on_source(self.obs_scene_name, self.obs_source_itemId, message.channel)
                self.cntFormanInsane = 0

        await self.handle_commands(message)

    async def switch_on_source(self, scene_name, scene_ItemId, channel):
        self.ws.call(requests.SetSceneItemEnabled(sceneItemId=scene_ItemId, sceneItemEnabled=True, sceneName=scene_name))
        print(f"[+] Switched on source: {scene_ItemId} in scene: {scene_name}")
        await channel.send(self.ttv_message)
        print(f"[+] Sleeping 120sec")
        time.sleep(120)
        print(f"[+] Disable Source ({scene_ItemId})")
        self.ws.call(requests.SetSceneItemEnabled(sceneItemId=scene_ItemId, sceneItemEnabled=False, sceneName=scene_name))


    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'hello {ctx.author.name}!')

bot = Bot()
bot.run()
