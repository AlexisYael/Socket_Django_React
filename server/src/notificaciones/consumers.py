import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.numero_usuario = self.scope['url_route']['kwargs']['numero_usuario']
        self.grupo_notificaciones = 'notificaciones_%s' % self.numero_usuario

        print(self.grupo_notificaciones)
        #Uirse a su grupo de notifcacioes
        await self.channel_layer.group_add(
            self.grupo_notificaciones,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.grupo_notificaciones,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        datos_json = json.loads(text_data)
        tipo_evento = datos_json['tipo']
        texto = datos_json['texto']
        usuario_destino = datos_json['destino']

        print(datos_json)

        if tipo_evento == 'notificar':
            grupo = 'notificaciones_%s' % usuario_destino   

            await self.channel_layer.group_add(
                grupo,
                self.channel_name
            )

            await self.channel_layer.group_send(
                grupo,
                {
                    'type' : 'notification',
                    'texto' : texto,
                    'destino' : usuario_destino
                }
            )

            await self.channel_layer.group_discard(
                grupo,
                self.channel_name
            )
        
        elif tipo_evento == 'chat':
            # Send message to room group
            await self.channel_layer.group_send(
                usuario_destino,
                {
                    'type': 'chat_message',
                    'texto': texto
                }
            )

        else:
            await self.disconnect(1234)

    # Receive message from room group
    async def chat_message(self, event):
        texto = event['texto']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'texto': texto
        }))

    async def notification(self,event):
        texto = event['texto']

        if(self.numero_usuario == event['destino']):
            await self.send(text_data = json.dumps({
                'texto' : texto
            }))



