import json
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.parsers import JSONParser,MultiPartParser
from detoxa_services.models.users import Users,Address
from detoxa_services.models.orders import Cart, Order
from detoxa_services.models.transactions_models import Invoice, OrderTransaction
from detoxa_services.serializers.order_serializer import CartSerializer, GetCartSerializer, GetOrderSerializer,CreateOrderSerializer, InvoiceSerializer, OrderListingForAdminSeriailizer,OrderTransactionSerializer, UpdateCartSerializer
from detoxa_services.tasks.generate_invoice_pdf import generate_invoice
from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from detoxa_services.views.subscription_views import createRazorPayOrder


class OrderListView(ListAPIView):
    serializer_class = GetOrderSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        queryset = Order.objects.filter(user=logged_in_user).order_by('-id')
        my_order = self.paginate_queryset(queryset)
        print(my_order, '+====')
        total_count = Order.objects.filter(user=logged_in_user).count()
        serializer = GetOrderSerializer(my_order, many=True)
        return Response({'data': serializer.data, "count": total_count}, status=HTTP_200_OK)


class CreateOrderView(CreateAPIView):
    serializer_class = CreateOrderSerializer
    # parser_classes = (MultiPartParser,)

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order_obj = Order.objects.create(user=logged_in_user,
                                             order_items=serializer.validated_data.get('order_items'),
                                             order_gst=serializer.validated_data.get('order_gst'),
                                             order_total_without_gst=serializer.validated_data.get('order_total_without_gst'),
                                             order_total=serializer.validated_data.get('order_total'),
                                             order_discount=serializer.validated_data.get('order_discount'),
                                             order_status=serializer.validated_data.get('order_status'),
                                             address=serializer.validated_data.get('address'),
                                             is_coupon_applied=serializer.validated_data.get('is_coupon_applied'),
                                             coupon_code=serializer.validated_data.get('coupon_code'),
                                             )
            razorpay_details = ''
            try:
                razorpay_details = createRazorPayOrder(float(serializer.validated_data.get('order_total')))
                if razorpay_details.status_code == 200:
                    razorpay_order_id = razorpay_details.json().get('id')
            except Exception as e:
                print(e)
            serializer = GetOrderSerializer(order_obj,many=False)
            return Response({'msg': 'Order created successfully', 'data': serializer.data,
                             'razorpay_details': razorpay_details.json()}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetOrderById(RetrieveAPIView):
    serializer_class = GetOrderSerializer

    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Order.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            serializer = GetOrderSerializer(queryset,many=False)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'msg':'Order does not exists'},status=HTTP_400_BAD_REQUEST)

class CancelOrdeView(UpdateAPIView):
    # serializer_class = GetOrderSerializer

    def put(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Order.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            queryset.order_status = 'Cancelled'
            queryset.save()
            return Response({'msg':'Order cancelled successfully'},status=HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'msg':'Order does not exists'},status=HTTP_400_BAD_REQUEST)


class CreateOrderTransactionView(CreateAPIView):
    serializer_class = OrderTransactionSerializer

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = OrderTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if OrderTransaction.objects.filter(order=serializer.validated_data.get('order')).exists():
                    return Response({'msg':'Transaction already exists'},status=HTTP_400_BAD_REQUEST)
                OrderTransaction.objects.create(user=logged_in_user,**serializer.validated_data)
                generate_invoice.delay(logged_in_user.id,serializer.validated_data.get('order').id)
                return Response({'msg':'Payment made successfully'},status=HTTP_200_OK)
            except Exception as e:
                return Response({'msg':str(e)},status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class GetOrderTransactionById(RetrieveAPIView):
    serializer_class = OrderTransactionSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = OrderTransaction.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            serializer = OrderTransactionSerializer(queryset,many=False)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except OrderTransaction.DoesNotExist:
            return Response({'msg':'Order transaction does not exists'},status=HTTP_400_BAD_REQUEST)

class OrderTransactionListView(ListAPIView):
    serializer_class = OrderTransactionSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        queryset = OrderTransaction.objects.filter(user=logged_in_user)
        serializer = OrderTransactionSerializer(queryset,many=True)
        return Response({'data':serializer.data},status=HTTP_200_OK)


class GetOrdersForAdmin(ListAPIView):
    serializer_class = OrderListingForAdminSeriailizer
    parser_classes = [MultiPartParser]
    pagination_class = StandardResultsSetPagination
    from_date = openapi.Parameter('from_date', openapi.IN_QUERY,type=openapi.TYPE_STRING,)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY,type=openapi.TYPE_STRING,)
    order_number = openapi.Parameter('order_number', openapi.IN_QUERY,type=openapi.TYPE_STRING,)
    order_status = openapi.Parameter('order_status', openapi.IN_QUERY, description="User class should be passed to get the list of reports generated based on their class.",required=False, type=openapi.TYPE_STRING, enum=['Pending','Confirmed','Cancelled','Dispatched','Out for Delivery','Delivered'])
    
    @swagger_auto_schema(manual_parameters=[from_date,to_date,order_number,order_status])
    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        order_number = request.query_params.get('order_number')
        order_status = request.query_params.get('order_status')
        if from_date and to_date:
            queryset = OrderTransaction.objects.filter(order__created_at__range=(from_date,to_date))
            page = self.paginate_queryset(queryset)
            serializer = OrderListingForAdminSeriailizer(page,many=True)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        if order_number:
            queryset = OrderTransaction.objects.filter(order__id=order_number)
            page = self.paginate_queryset(queryset)
            serializer = OrderListingForAdminSeriailizer(page,many=True)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        if order_status:
            queryset = OrderTransaction.objects.filter(order__order_status=order_status)
            page = self.paginate_queryset(queryset)
            serializer = OrderListingForAdminSeriailizer(page,many=True)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        if logged_in_user.is_admin:
            queryset = OrderTransaction.objects.all()
            page = self.paginate_queryset(queryset)
            serializer = OrderListingForAdminSeriailizer(page,many=True)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        return Response({'msg':'You are not authorized to access this page'},status=HTTP_400_BAD_REQUEST)

class GetOrderByIdForAdmin(RetrieveAPIView):
    serializer_class = OrderListingForAdminSeriailizer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                queryset = OrderTransaction.objects.get(id=self.kwargs['pk'])
                serializer = OrderListingForAdminSeriailizer(queryset,many=False)
                return Response({'data':serializer.data},status=HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'msg':'Order does not exists'},status=HTTP_400_BAD_REQUEST)
        return Response({'msg':'You are not authorized to access this page'},status=HTTP_400_BAD_REQUEST)


class UpdateOrderStatusForAdmin(UpdateAPIView):
    # serializer_class = OrderListingForAdminSeriailizer
    order_status = openapi.Parameter('order_status', openapi.IN_QUERY, description="Order status should be passed to update the order status.",required=True, type=openapi.TYPE_STRING, enum=['Pending','Confirmed','Cancelled','Dispatched','Out for Delivery','Delivered'])
    
    @swagger_auto_schema(manual_parameters=[order_status])
    def put(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                queryset = OrderTransaction.objects.get(id=self.kwargs['pk'])
                queryset.order.order_status = request.query_params.get('order_status')
                queryset.order.save()
                return Response({'msg':'Order status updated successfully'},status=HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'msg':'Order does not exists'},status=HTTP_400_BAD_REQUEST)
        return Response({'msg':'You are not authorized to access this page'},status=HTTP_400_BAD_REQUEST)


class GetCartItems(ListAPIView):
    serializer_class = GetCartSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        queryset = Cart.objects.filter(user=logged_in_user)
        serializer = GetCartSerializer(queryset,many=True)
        return Response({'data':serializer.data,'item_count':queryset.count()},status=HTTP_200_OK)

class AddItemToCart(CreateAPIView):
    serializer_class = CartSerializer

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if serializer.data['quantity'] > 0:
                    if Cart.objects.filter(user=logged_in_user,item=serializer.data['item']).exists():
                        cart_obj = Cart.objects.get(user=logged_in_user,item=serializer.data['item'])
                        cart_obj.quantity = cart_obj.quantity + serializer.data['quantity']
                        cart_obj.save()
                    else:
                        Cart.objects.create(user=logged_in_user,item=serializer.validated_data['item'],quantity=serializer.validated_data['quantity'])
                    return Response({'msg':'Item added to cart successfully'},status=HTTP_200_OK)
                else:
                    return Response({'msg':'Quantity should be greater than 0'},status=HTTP_400_BAD_REQUEST)
            except Cart.DoesNotExist:
                return Response({'msg':'Item does not exists'},status=HTTP_400_BAD_REQUEST)
        return Response({'msg':'Item could not be added to cart'},status=HTTP_400_BAD_REQUEST)

class RemoveItemFromCart(DestroyAPIView):
    serializer_class = CartSerializer

    def delete(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Cart.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            queryset.delete()
            return Response({'msg':'Item removed from cart successfully'},status=HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'msg':'Item does not exists'},status=HTTP_400_BAD_REQUEST)

class UpdateCartItem(UpdateAPIView):
    serializer_class = UpdateCartSerializer

    def put(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Cart.objects.get(user=logged_in_user,id=self.kwargs['pk'])
            serializer = UpdateCartSerializer(queryset,data=request.data)
            if serializer.is_valid():
                queryset.quantity = serializer.validated_data['quantity']
                queryset.save()
                return Response({'msg':'Item updated successfully'},status=HTTP_200_OK)
            return Response({'msg':'Item could not be updated'},status=HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'msg':'Item does not exists'},status=HTTP_400_BAD_REQUEST)

class GetCartItemDetails(RetrieveAPIView):
    serializer_class = GetCartSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            queryset = Cart.objects.get(user=logged_in_user,id=self.kwargs['pk']).order_by('-id')
            serializer = GetCartSerializer(queryset,many=False)
            return Response({'data':serializer.data},status=HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'msg':'Item does not exists'},status=HTTP_400_BAD_REQUEST)


class GetInvoices(ListAPIView):
    serializer_class = InvoiceSerializer

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        queryset = Invoice.objects.filter(user=logged_in_user)
        serializer = InvoiceSerializer(queryset,many=True)
        return Response({'data':serializer.data},status=HTTP_200_OK)


class ClearCartAPIView(CreateAPIView):

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        for i in Cart.objects.filter(user=logged_in_user):
            i.delete()
        return Response({'msg':'Cart cleared successfully'},status=HTTP_200_OK)