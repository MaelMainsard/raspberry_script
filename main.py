from peewee import *
from models import NodeParam,NodeData
import os
from dotenv import load_dotenv
import paho.mqtt.publish as publish
import datetime

load_dotenv()

db_dir = './db'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"Dossier {db_dir} créé avec succès.")

db_path = os.path.join(db_dir, 'zigbee.db')

db = SqliteDatabase(db_path)

if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
    print(f"Création de la base de données {db_path}")
    db.connect()
    db.create_tables([NodeParam, NodeData])
    print("Tables créées avec succès.")

auth = {
    "username": "user",
    "password": os.getenv('MQTT_TOKEN')
}

def manage_node():
    count = NodeParam.select().where(NodeParam.name == "esp32 room 1").count()

    if count > 0:
        existing_node = NodeParam.select().where(NodeParam.name == "esp32 room 1").get()
        existing_node.updated_at = datetime.datetime.now()
        existing_node.save()
        return existing_node
    else:
        new_node = NodeParam.create(name='esp32 room 1')
        return new_node
def get_data_to_send(node, data):
    new_temp = data["temp"]
    new_hum = data["hum"]

    query = (NodeData.select(
        fn.COUNT(NodeData.id).alias('count'),
        fn.SUM(NodeData.temperature).alias('temperature'),
        fn.SUM(NodeData.humidity).alias('humidity'),
    )
    .where(NodeData.node_id == node.id))

    result = query.get()

    if result.count > 0:
        total_count = result.count + 1
        avg_temperature = round((result.temperature + new_temp) / total_count, 1)
        avg_humidity = round((result.humidity + new_hum) / total_count, 1)
    else:
        avg_temperature = round(new_temp, 1)
        avg_humidity = round(new_hum, 1)

    return {
        "temperature": avg_temperature,
        "humidity": avg_humidity
    }
def save_data(node, temp, hum):
    NodeData.create(node_id=node.id, temperature=temp, humidity=hum)
def format_payload(node,data):
    payload = {
        "node_id": str(node.id),
        "node_name": node.name,
        "data": data,
    }
    return str(payload)


def main():
    db.connect()
    db.create_tables([NodeParam, NodeData], safe=True)

    my_node = manage_node()
    new_data = {
        "temp": 23.6,
        "hum": 56.3
    }

    data_to_send = get_data_to_send(my_node, new_data)

    try :
        publish.single(os.getenv("MQTT_TOPIC"), format_payload(my_node,data_to_send),  hostname=os.getenv("MQTT_HOSTNAME"), port=int(os.getenv("MQTT_PORT")), auth=auth)
    except Exception as e :
        save_data(my_node, 23.6, 56.3)


if __name__ == '__main__':
    main()