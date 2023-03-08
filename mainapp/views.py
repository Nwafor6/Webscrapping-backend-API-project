from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
import requests
from .serializers import JobSerializer
from .models import Job
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class LatestJobs(APIView):
    """
    fetch all the list of jobs from jobberman
    """
    def get(self, request):
        
        r=requests.get('https://www.jobberman.com/jobs/software-data').text
        soup=BeautifulSoup(r,"lxml")
        jobs=soup.find_all('div', class_="mx-5 md:mx-0 flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500")
        Job.objects.all().delete()
        for job in jobs:
            try:
                job_title=job.find("p", class_="text-lg font-medium break-words text-brand-linked").text
            except:
                pass
            try:
                company_name=job.find('p',class_="text-sm text-brand-linked").contents[0]
            except:
                pass
            try:
                company_name=company_name.contents[0]
            except:
                pass
            try:
                location=job.find("div", class_="flex flex-wrap mt-3 text-sm text-gray-500 md:py-0").contents[0]
            except:
                pass
            try:
             location=location.contents[0]
            except:
                pass
            try:
                job_nature=job.find("div", class_="flex flex-wrap mt-3 text-sm text-gray-500 md:py-0").contents[1]
            except:
                pass
            try:
                job_nature=job_nature.contents[0]
            except:
                pass
            try:
                job_pay=job.find("div", class_="flex flex-wrap mt-3 text-sm text-gray-500 md:py-0").contents[2]
            except:
                pass
            try:
                joy_currency=job_pay.contents[0].text
            except:
                pass
            try:
                job_pay=job_pay.contents[1].text
            except:
                job_pay=""
            posted=job.find("p",class_="ml-auto text-sm font-normal text-gray-700 text-loading-animate").text
            job_summary=job.find("p", class_="text-sm font-normal text-gray-700 md:text-gray-500 md:pl-5").text
            read_more=job.find("div", class_="flex items-center")
            read_more=read_more.a["href"]
            try:
                job=Job.objects.get(
                job_title=job_title,
                company_name=company_name,
                location=location,
                job_nature=job_nature,
                job_pay=job_pay,
                joy_currency=joy_currency,
                posted=posted,
                job_summary=job_summary,
                read_more=read_more,
                )
            except:
                job=Job.objects.create(job_title=job_title.strip(),company_name=company_name.strip(),location=location.strip(),
                job_nature=job_nature.strip(),job_pay=job_pay.strip(),joy_currency=joy_currency.strip(),posted=posted.strip(),job_summary=job_summary.strip(),read_more=read_more.strip(),
                )
        jobs=Job.objects.all()
        # For filtering from the front end
        _job_stack=[]
        _job_nature=[]
        job_location=[]
        for job in jobs:
            if job.job_title not in _job_stack:
                _job_stack.append(job.job_title)
            if job.job_nature not in _job_nature:
                _job_nature.append(job.job_nature)

            if job.location not in job_location:
                job_location.append(job.location)
        serializer=JobSerializer(jobs, many=True)
        return Response({"data":serializer.data, "job_nature":_job_nature, "job_location":job_location, "job_stack":_job_stack})

@csrf_exempt
@api_view(["POST"])
def filterjobView(request):
    location=request.POST["location"]
    job_nature=request.POST["job_nature"]
    job_title=request.POST["job_stack"]
    jobs=Job.objects.filter(location=location,job_nature=job_nature, job_title=job_title)
    serializer=JobSerializer(jobs, many=True)
    return Response({"data":serializer.data, })

@csrf_exempt
@api_view(["POST"])
def DetailedPageView(request):
    r=requests.get(f'{request.POST["link"]}').text
    soup=BeautifulSoup(r,"lxml")
    job=soup.find('article', class_="job__details")
    job_title=job.find("h1", class_="mt-6 mb-3 text-lg font-medium text-gray-700 md:mb-4 md:mt-0").text.strip()
    company_name=job.find("a", class_="text-brand-linked").text.strip()
    posted=job.find("div", class_="flex relative justify-end pl-3 text-gray-500 font-sm ml-auto").text.strip()
    job_nature=job.find("span", class_="text-sm font-normal px-3 rounded bg-brand-opaque mr-2 mb-3 inline-block").a.text.strip()
    job_summary=job.find("p", class_="mb-4 text-sm text-gray-500").text.strip()
    job_responsibility=job.find("ul", class_="list-disc list-inside").contents
    responsibility=[]
    for i in job_responsibility:
        responsibility.append(i.text.strip())

    return Response({"responsibility":responsibility, "job_title":job_title,
                        "company_name":company_name, "posted":posted,"job_nature":job_nature,"job_summary":job_summary})
    