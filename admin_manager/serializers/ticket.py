from rest_framework import serializers
from ..models import Ticket, Campaign, MailTrack, Contact, User, Order


class TicketSerializer(serializers.ModelSerializer):
    # Thêm trường để nhận order_id từ payload
    order_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Ticket
        fields = '__all__'  # Hoặc chỉ định cụ thể các trường bạn muốn sử dụng
        extra_kwargs = {
            # Tránh yêu cầu trường này từ payload
            'order': {'read_only': True},
        }

    def create(self, validated_data):
        order_id = validated_data.pop('order_id', None)
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                {"order_id": "Order with this ID does not exist."})

        validated_data['order'] = order
        return super().create(validated_data)

    def update(self, instance, validated_data):
        order_id = validated_data.pop('order_id', None)
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                {"order_id": "Order with this ID does not exist."})
        
        # Cập nhật liên kết order
        instance.order = order

        # Cập nhật các trường khác
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Lưu đối tượng
        instance.save()
        return instance


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class MailTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTrack
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_staff",
            "date_joined",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "address",
            "department_code",
            "user_type",
            "created_date",
        ]
        extra_kwargs = {
            # Bỏ qua trường user khi validation
            'is_staff': {'required': False}
        }


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # Nested UserSerializer to include full user details
    owner = UserSerializer(required=False)  # Nested UserSerializer to include full user details

    class Meta:
        model = Contact
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},  # Bỏ qua trường user khi validation
            'owner': {'required': False}  # Bỏ qua trường user khi validation
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
