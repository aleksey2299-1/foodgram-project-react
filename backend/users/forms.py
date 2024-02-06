from django import forms

from users.models import CustomBaseUser


class UserThroughForm(forms.ModelForm):
    """Form for admin panel."""
    from_custombaseuser = forms.ModelChoiceField(
        queryset=CustomBaseUser.objects.all(),
        label='Пользователь',
        required=True,
    )
    to_custombaseuser = forms.ModelChoiceField(
        queryset=CustomBaseUser.objects.all(),
        label='Подписан на',
        required=True,
    )

    class Meta:
        model = CustomBaseUser.subscribe.through
        fields = ('from_custombaseuser', 'to_custombaseuser')
