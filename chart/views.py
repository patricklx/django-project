from django.shortcuts import render


def show_chart(request):
    return render(template_name='chart.html', request=request)