from django.urls import path
from . import views

app_name = 'burp_suite_suite'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('scanner/', views.scanner, name='scanner'),
    path('scanner/start/', views.start_scan, name='start_scan'),
    path('scanner/<int:scan_id>/status/', views.scan_status, name='scan_status'),
    path('scanner/<int:scan_id>/detail/', views.scan_detail, name='scan_detail'),
    path('scanner/<int:scan_id>/delete/', views.delete_scan, name='delete_scan'),
    path('proxy/', views.proxy, name='proxy'),
    path('proxy/toggle/', views.intercept_toggle, name='intercept_toggle'),
    path('proxy/intercept-status/', views.intercept_status, name='intercept_status'),
    path('proxy/history/', views.proxy_history, name='proxy_history'),
    path('proxy/add/', views.add_proxy_request, name='add_proxy_request'),
    path('proxy/clear/', views.clear_proxy_history, name='clear_proxy_history'),
    path('proxy/intercept/', views.intercept_request, name='intercept_request'),
    path('proxy/<int:req_id>/forward/', views.forward_request, name='forward_request'),
    path('proxy/<int:req_id>/drop/', views.drop_request, name='drop_request'),
    path('proxy/<int:req_id>/delete/', views.delete_proxy_request, name='delete_proxy_request'),
    path('proxy/<int:req_id>/modify/', views.modify_and_forward, name='modify_and_forward'),
    path('proxy/<int:req_id>/release/', views.release_request, name='release_request'),
    path('proxy/action/', views.proxy_action, name='proxy_action'),
    path('intruder/', views.intruder, name='intruder'),
    path('intruder/run/', views.run_intruder, name='run_intruder'),
    path('intruder/<int:intruder_id>/status/', views.intruder_status, name='intruder_status'),
    path('intruder/add-payload/', views.add_payload, name='add_payload'),
    path('repeater/', views.repeater, name='repeater'),
    path('repeater/send/', views.send_repeater, name='send_repeater'),
    path('spider/', views.spider, name='spider'),
    path('spider/start/', views.start_spider, name='start_spider'),
    path('decoder/', views.decoder, name='decoder'),
    path('decoder/encode/', views.decode_encode, name='decode_encode'),
    path('comparer/', views.comparer, name='comparer'),
    path('comparer/compare/', views.compare_data, name='compare_data'),
]