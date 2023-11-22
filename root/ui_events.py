from types import FunctionType
import _dbg as dbg

class UiEvents(dict):
    def GetEvent(self, event_name:str) -> FunctionType:
        if not event_name in self:
            return None
        return self[event_name]['event']

    def GetArguments(self, event_name:str) -> tuple:
        if not event_name in self:
            return ()
        return self[event_name]['args']

    def SetEvent(self, window_name:str, event_name:str, event:FunctionType, *args) -> None:
        self.update({event_name:{'event':event, 'args':args, 'window_name':window_name}})

    def DeleteEvent(self, event_name:str):
        del self[event_name]

    def ExecuteEvent(self, event_name:str) -> bool:
        event_dict = self.get(event_name)
        if not event_dict:
            return False

        event = event_dict['event']
        args = event_dict['args']
        window_name = event_dict['window_name']

        dbg.TraceError(f'{event_name} window_name: {window_name} func: {event} args: {args}')
        event(*args)
        return True
