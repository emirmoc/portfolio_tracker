APIS = [{
    'field_name': 'SymbolDescription',
    'field_price': 'AvgPrice',
    'field_symbol': 'Symbol',
    'name': 'SASE',
    'root': 'http://www.sase.ba',
    'params': { 'type': 19 },
    'request_type': "POST",
    'status': 'FeedServices/HandlerChart.ashx',
    'type': 'json'
}, {
    'field_name': 'Description',
    'field_price': 'AvgPrice',
    'field_symbol': 'Code',
    'name': 'BL berza',
    'root': 'https://www.blberza.com',
    'params': { 'langId': 1 },
    'request_type': "GET",
    'status': 'services/defaultTicker.ashx',
    'type': 'json'
}]