from datetime import datetime, date, timedelta

def next_code(prefix:str, count:int)->str:
    return f"{prefix}-{count+1:04d}"

def invoice_status(total:float, paid:float, due_date:date):
    saldo = max(total-paid, 0)
    if saldo <= 0:
        return 'Pagada', 0
    if paid > 0:
        if due_date and due_date < date.today():
            return 'Vencida', saldo
        return 'Parcial', saldo
    if due_date and due_date < date.today():
        return 'Vencida', saldo
    return 'Pendiente', saldo

CHECKLISTS = {
    'Instalación cámaras': ['Confirmar ubicación de cámaras','Revisar cableado','Revisar alimentación','Configurar NVR/DVR','Configurar visualización en celular','Probar grabación','Probar visión nocturna','Explicar uso al cliente','Tomar fotos antes/después','Registrar garantía','Firma de entrega'],
    'Cerco eléctrico': ['Revisar perímetro','Revisar aisladores','Revisar energizador','Revisar tierra física','Probar sirena','Probar batería','Explicar uso al cliente','Tomar fotos','Firma de entrega'],
    'Redes': ['Revisar router','Revisar puntos de red','Etiquetar cableado','Probar velocidad','Probar cobertura WiFi','Entregar claves al cliente','Tomar evidencias','Firma de entrega']
}
