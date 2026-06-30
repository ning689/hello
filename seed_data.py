"""
?????? - ???????
??: python seed_data.py
"""
import os, sys, django
from datetime import datetime, timedelta
from decimal import Decimal
import random, string

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courier_system.settings')
django.setup()

from django.utils import timezone
from users.models import User, Address
from stations.models import Branch, Station, Shelf
from orders.models import Order
from tracking.models import TrackingLog
from couriers.models import CourierProfile, DeliveryTask
from pricing.models import FreightTemplate, FreightRule, InsuranceRate
from notifications.models import NotificationTemplate
from stations.models import StationInventory

def seed():
    print("???????...")

    # === 1. ???? ===
    branch1 = Branch.objects.get_or_create(name='????????', defaults={
        'address': '???????????1?', 'contact_person': '???',
        'contact_phone': '0755-88886666', 'province': '???', 'city': '???', 'district': '???'
    })[0]
    branch2 = Branch.objects.get_or_create(name='????????', defaults={
        'address': '??????????100?', 'contact_person': '???',
        'contact_phone': '0755-88887777', 'province': '???', 'city': '???', 'district': '???'
    })[0]
    print(f"? ????: {branch1.name}, {branch2.name}")

    # === 2. ???? ===
    station1 = Station.objects.get_or_create(name='???????', defaults={
        'branch': branch1, 'address': '?????A?1?', 'contact_phone': '13800138001',
    })[0]
    station2 = Station.objects.get_or_create(name='???????', defaults={
        'branch': branch1, 'address': '?????B2?', 'contact_phone': '13800138002',
    })[0]
    station3 = Station.objects.get_or_create(name='???????', defaults={
        'branch': branch2, 'address': '???????1?', 'contact_phone': '13800138003',
    })[0]
    print(f"? ????: {station1.name}, {station2.name}, {station3.name}")

    # === 3. ???? ===
    for station in [station1, station2, station3]:
        for zone in ['A', 'B', 'C']:
            for num in range(1, 4):
                Shelf.objects.get_or_create(station=station, shelf_no=f'{zone}-{num:02d}', defaults={'zone': zone})
    print("? ????")

    # === 4. ???? ===
    users_data = {
        'admin': {'password': 'admin123', 'phone': '13900000001', 'role': 'admin', 'branch': None},
        'courier1': {'password': '123456', 'phone': '13800138101', 'role': 'courier', 'branch': branch1},
        'courier2': {'password': '123456', 'phone': '13800138102', 'role': 'courier', 'branch': branch2},
        'station1': {'password': '123456', 'phone': '13800138201', 'role': 'station_admin', 'branch': branch1},
        'station2': {'password': '123456', 'phone': '13800138202', 'role': 'station_admin', 'branch': branch2},
        'user1': {'password': '123456', 'phone': '13800138301', 'role': 'user', 'branch': None},
        'user2': {'password': '123456', 'phone': '13800138302', 'role': 'user', 'branch': None},
    }
    created_users = {}
    for username, data in users_data.items():
        user, is_new = User.objects.get_or_create(username=username, defaults={
            'phone': data['phone'], 'role': data['role'], 'branch': data['branch']
        })
        if is_new:
            user.set_password(data['password'])
            user.save()
        created_users[username] = user
    print(f"? ????: {', '.join(created_users.keys())}")

    # === 5. ??????? ===
    for username, emp_id in [('courier1', 'SF001'), ('courier2', 'SF002')]:
        CourierProfile.objects.get_or_create(user=created_users[username], defaults={
            'employee_id': emp_id, 'id_card': '44030119900101xxxx', 'vehicle_type': 'electric_bike'
        })
    print("? ???????")

    # === 6. ?????? ===
    order_templates = [
        {'sender': '??', 'sender_phone': '13912345678', 'receiver': '??', 'receiver_phone': '13698765432',
         'sender_addr': ('???', '???', '???', '?????10?'), 'receiver_addr': ('???', '???', '???', '????????66?'),
         'weight': 1.5, 'goods': '????', 'desc': '?????', 'status': 'delivered'},
        {'sender': '??', 'sender_phone': '13711112222', 'receiver': '??', 'receiver_phone': '15833334444',
         'sender_addr': ('???', '???', '???', '????200?'), 'receiver_addr': ('???', '???', '????', '??SOHO T1'),
         'weight': 0.8, 'goods': '??', 'desc': '????', 'status': 'in_transit'},
        {'sender': '??', 'sender_phone': '13655556666', 'receiver': '??', 'receiver_phone': '15977778888',
         'sender_addr': ('???', '???', '???', '????88?'), 'receiver_addr': ('???', '????', '???', '??????20?'),
         'weight': 3.2, 'goods': '??', 'desc': '??????', 'status': 'waiting_pickup'},
        {'sender': '??', 'sender_phone': '13599990000', 'receiver': '??', 'receiver_phone': '18611112222',
         'sender_addr': ('???', '???', '???', '????55?'), 'receiver_addr': ('???', '???', '???', '???100?'),
         'weight': 5.0, 'goods': '???', 'desc': '????', 'status': 'exception'},
    ]

    status_map = {
        'waiting_pickup': Order.OrderStatus.WAITING_PICKUP,
        'in_transit': Order.OrderStatus.IN_TRANSIT,
        'delivered': Order.OrderStatus.DELIVERED,
        'exception': Order.OrderStatus.EXCEPTION,
    }

    order_objs = []
    for i, t in enumerate(order_templates):
        order_no = f'EX{datetime.now().strftime("%Y%m%d")}{"".join(random.choices(string.digits, k=6))}'
        tracking_id = f'SF{datetime.now().strftime("%y%m%d")}{"".join(random.choices(string.digits, k=8))}'

        order = Order.objects.create(
            order_no=order_no, tracking_id=tracking_id,
            sender_name=t['sender'], sender_phone=t['sender_phone'],
            sender_province=t['sender_addr'][0], sender_city=t['sender_addr'][1],
            sender_district=t['sender_addr'][2], sender_address=t['sender_addr'][3],
            receiver_name=t['receiver'], receiver_phone=t['receiver_phone'],
            receiver_province=t['receiver_addr'][0], receiver_city=t['receiver_addr'][1],
            receiver_district=t['receiver_addr'][2], receiver_address=t['receiver_addr'][3],
            weight=Decimal(str(t['weight'])), goods_type=t['goods'], goods_desc=t['desc'],
            freight_fee=Decimal(str(10 + max(0, t['weight']-1)*5)),
            total_fee=Decimal(str(10 + max(0, t['weight']-1)*5)),
            express_company='SF', user=created_users['user1'],
            order_status=status_map[t['status']],
        )

        # ????
        TrackingLog.objects.create(order=order, tracking_id=tracking_id,
            status='created', status_desc='?????', operator='??',
            operate_time=timezone.now() - timedelta(hours=random.randint(1, 48)))

        # ??????????
        if t['status'] in ['in_transit', 'delivered']:
            TrackingLog.objects.create(order=order, tracking_id=tracking_id,
                status='picked_up', status_desc='??????', operator='???',
                operate_time=timezone.now() - timedelta(hours=random.randint(6, 24)))
            TrackingLog.objects.create(order=order, tracking_id=tracking_id,
                status='in_transit', status_desc='?????????', operator='??',
                location=f'{t["sender_addr"][1]}????',
                operate_time=timezone.now() - timedelta(hours=random.randint(2, 12)))

        if t['status'] == 'delivered':
            TrackingLog.objects.create(order=order, tracking_id=tracking_id,
                status='delivering', status_desc='??????', operator='???',
                operate_time=timezone.now() - timedelta(hours=random.randint(1, 4)))
            TrackingLog.objects.create(order=order, tracking_id=tracking_id,
                status='delivered', status_desc='???', operator='???',
                location=t['receiver_addr'][3],
                operate_time=timezone.now() - timedelta(hours=random.randint(0, 2)))

        order_objs.append(order)
        print(f"  ? ????: {order_no} ({t['status']})")

    print(f"? ?? {len(order_objs)} ?????")

    # === 7. ??????? ===
    for order in order_objs[:2]:
        task_type = 'pickup' if order.order_status in ['waiting_pickup', 'in_transit'] else 'deliver'
        DeliveryTask.objects.get_or_create(
            courier=created_users['courier1'], order=order,
            defaults={'task_type': task_type, 'status': 'completed' if order.order_status == 'delivered' else 'pending'}
        )
    print("? ???????")

    # === 8. ?????? ===
    template = FreightTemplate.objects.get_or_create(
        name='??????', express_company='SF',
        defaults={
            'mode': 'weight', 'first_weight': 1, 'first_price': 12,
            'additional_weight': 1, 'additional_price': 6,
            'effective_date': timezone.now().date(),
        }
    )[0]
    FreightRule.objects.get_or_create(template=template, province='???',
        defaults={'first_price_override': 10, 'additional_price_override': 5})
    print("? ??????")

    # === 9. ?????? ===
    NotificationTemplate.objects.get_or_create(name='????', channel='sms',
        defaults={'template_id': 'SMS_001', 'content_template': '???????{station}?????{pick_code}????{address}'})
    print("? ??????")

    print("\n" + "="*40)
    print("?  ???????!")
    print("="*40)
    print("\n?????")
    print("  ???: admin / admin123")
    print("  ???: courier1 / 123456")
    print("  ??:   station1 / 123456")
    print("  ??:   user1 / 123456")
    print("\n????: http://127.0.0.1:8000/")

if __name__ == '__main__':
    seed()
