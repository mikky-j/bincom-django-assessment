from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from itertools import chain

# Create your views here.


def index(request):
    return render(request, "main/home.html", {})

def question1(request):
    polling_units = set()
    for results in AnnouncedPuResults.objects.all():
        polling_units.add(results.polling_unit_uniqueid)
    polling_units = sorted(polling_units, key=lambda x: int(x))
    polling_units = list(map(lambda x: PollingUnit.objects.get(uniqueid=int(x)), polling_units))

    return render(request, "main/question1.html", {"polling_units": polling_units})

def question1_info(request, id):
    name = PollingUnit.objects.get(uniqueid=id).polling_unit_name
    announced_pu_results = list(AnnouncedPuResults.objects.filter(polling_unit_uniqueid=id))
    return render(request, "main/question1_info.html", {"units": announced_pu_results, "name": name})

def question2(request):
    lgas = Lga.objects.all()
    return render(request, "main/question2.html", {"lgas": lgas})

def _get_results_from_units(unit):
    try:
        print(unit.uniqueid)
        return  AnnouncedPuResults.objects.filter(polling_unit_uniqueid=unit.uniqueid) 
    except AnnouncedPuResults.DoesNotExist:
        return None

def question2_info(request, id):
    name = Lga.objects.get(lga_id=id).lga_name
    polling_units = PollingUnit.objects.filter(lga_id=id)
    results_of_all_polling_units = map(_get_results_from_units, polling_units)
    raw_results = chain(*results_of_all_polling_units)
    calculated_results = dict()
    for results in raw_results:
        if results != None:
            abbv = results.party_abbreviation
            if abbv in calculated_results:
                calculated_results[abbv] += int(results.party_score)
            else:
                calculated_results[abbv] = int(results.party_score)
            
    return render(request, "main/question2_info.html", {"results": calculated_results, "name": name, "length": len(calculated_results)})

def question3(request):
    parties = Party.objects.all()
    if request.method == "POST":
        from datetime import date
        data = request.POST
        
        polling_unit = PollingUnit.objects.create(
            polling_unit_name=data["p_name"],
            polling_unit_id=max(PollingUnit.objects.all(), key=lambda x: x.polling_unit_id).polling_unit_id+1,
            ward_id=data["ward"],
            lga_id=data["lga"],
            date_entered= date.today(),
            entered_by_user="king-mikky"
        )
        polling_unit.save()

        for party in parties:
            # WHY ARE YOU GUYS SO STUPID LIKE WHY IS YOUR DATABASE SO TRASH
            if len(party.partyname) < 5:
                result = AnnouncedPuResults.objects.create(
                    polling_unit_uniqueid=polling_unit.uniqueid,
                    party_abbreviation=party.partyname,
                    party_score=int(data[party.partyname]),
                    entered_by_user="king-mikky",
                    date_entered=polling_unit.date_entered,
                    user_ip_address="127.0.0.1"
                )
                result.save()
                # print(result.result_id)

        return  HttpResponseRedirect("%i/success" % polling_unit.uniqueid)
    else:
        wards = Ward.objects.all()
        lgas = Lga.objects.all()
        return render(request, "main/question3.html", {"lgas": lgas, "wards": wards, "parties": parties})

def question3_success(request, id):
    name = PollingUnit.objects.get(uniqueid=id).polling_unit_name
    return render(request, "main/question3_success.html", {"name": name})