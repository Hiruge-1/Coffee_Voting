from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Coffee,Voting
from django.db.models import Avg

class IndexView(generic.ListView):
    model = Coffee

class DetailView(generic.DetailView):
    model = Coffee
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results=Voting.objects.filter(coffee_id=self.kwargs['pk'])
        bitterness_result=results.aggregate(Avg('bitterness'))
        context['bitterness_avg']=bitterness_result['bitterness__avg']
        sourness_result=results.aggregate(Avg('sourness'))
        context['sourness_avg'] =sourness_result['sourness__avg']
        sweetness_result=results.aggregate(Avg('sweetness'))
        context['sweetness_avg'] =sweetness_result['sweetness__avg']
        richness_result=results.aggregate(Avg('richness'))
        context['richness_avg'] =richness_result['richness__avg']
        flavor_result=results.aggregate(Avg('flavor'))
        context['flavor_avg'] =flavor_result['flavor__avg']
        context['reviews']=results.values_list('review', flat=True)
        return context

class Coffee_CreateView(generic.edit.CreateView):
    model = Coffee
    fields = '__all__'

class UpdateView(generic.edit.UpdateView):
    model = Coffee
    fields = '__all__'

class DeleteView(generic.edit.DeleteView):
    model = Coffee
    success_url = reverse_lazy('coffee_voting:index')

class VotingView(generic.edit.CreateView):
    model = Voting
    fields = ['bitterness','sourness','sweetness','richness','flavor','review']
    template_name="coffee_voting/coffee_voting.html"
    
    #対応するCoffee.idの自動格納
    def form_valid(self, form):
        table = get_object_or_404(Coffee, pk=self.kwargs.get('pk'))
        form.instance.coffee_id = table
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coffee_name']=Coffee.objects.filter(pk=self.kwargs['pk']).first()
        return context
