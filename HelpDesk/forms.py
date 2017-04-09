from django import forms
from .models import Request, Users, TaskList,Structure
from django.forms.widgets import Select


choices=(
    ('Оборудование', (
        ('1', 'Установка принтера'),
        ('2', 'Настроить сетевой принтер'),
        ('3', 'Установить драйвера'),
        ('4', 'Диагностика принтера'),
        ('5', 'Настроить сканер'),
        ('6', 'Настроить МФУ'),
        ('7', 'Заправить картридж'),
        ('8', 'Заменить картридж'),
    )),
    ('Программное обеспечение', (
        ('9', 'Переустановить ОС'),
        ('10', 'Диагностика ПК'),
        ('11', 'Установить ПО'),
        ('12', 'Настройка интернет-соединения'),
        ('13', 'Диагностика интернет-соединения'),
        ('14', 'Проверка на вирусы'),
        ('15', 'Обновить ПО'),
        ('16', 'Устранить неполадки ПО'),
    )),
    ('Сети и интеренет телефония', (
        ('17', 'Подключение ПК к сети'),
        ('18', 'Подключить телефон'),
        ('19', 'Подключить междугороднюю связь'),
        ('20', 'Устранить причину неполадки телефона'),
    )),
    ('Сопровождение мероприятий', (
        ('21', 'Проектор'),
        ('22', 'Экран'),
        ('23', 'Звук(колонки, микшер)'),
        ('24', 'Микрофоны'),
        ('25', 'Аудиозапись'),
    )),
)

class RequestForm(forms.ModelForm):
    chief = forms.ModelChoiceField(Users.objects.filter(supervisor=True))
    tasks = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=choices
    )
    class Meta:
        model = Request
        fields = ('__all__')
        
class WorkerRequestForm(RequestForm):
    chief = forms.ModelChoiceField(Users.objects.filter(supervisor=True), disabled=True ,required=False)
    phone_number =  forms.CharField(disabled=True, required=False)
    client =  forms.CharField(disabled=True, required=False)
    receipt =  forms.DateField(disabled=True, required=False)
    comments = forms.CharField(disabled=True, required=False)
    office =  forms.CharField(disabled=True, required=False)
    structure = forms.ModelChoiceField(Structure.objects, disabled=True, required=False)
    tasks = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=choices,disabled=True ,required=False)
    worker = forms.ModelChoiceField(Users.objects, disabled=True)

    class Meta(RequestForm.Meta):
        exclude = ['tasks']
        fields = ('__all__')

class ClientRequestForm(RequestForm):
    chief= None
    class Meta(RequestForm.Meta):
        exclude = ['chief', 'worker', 'request_status', 'task_other', 'report', 'receipt', 'complete', 'call']
