from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import AccountInfoSerializer, AccountDetailSerializer
from .models import Account

@api_view(['GET'])
def list_accounts(request):
    accounts = Account.objects.all()
    serializer = AccountInfoSerializer(accounts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def signup_accounts(request):
    serializer = AccountDetailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
def detail_accounts(request, account_pk):
    account = get_object_or_404(Account, pk=account_pk)
    serializer = AccountDetailSerializer(account)
    return Response(serializer.data)