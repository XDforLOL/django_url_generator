
import json
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponseRedirect, HttpRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_utils.url_manager_utils import is_valid_url, url_hasher

from .models import Url, Redirect

logger = logging.getLogger(__name__)

@csrf_exempt
def create_short_url(request: 'HttpRequest') -> JsonResponse:

    if request.method != 'POST':
        return JsonResponse(data={'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        long_url = data.get('url')

    except (json.JSONDecodeError, KeyError):
        return JsonResponse(data={'error': 'URL parameter is required'}, status=400)

    if not long_url:
        return JsonResponse(data={'error': 'URL parameter is required'}, status=400)

    if not is_valid_url(long_url):
        return JsonResponse(data={'error': 'Invalid URL'}, status=400)

    short_endpoint = url_hasher(long_url)
    url_entry, created = Url.objects.get_or_create(short_endpoint=short_endpoint, long_url=long_url,
                                                   defaults={'short_endpoint': short_endpoint})

    return JsonResponse({'short_url': url_entry.short_endpoint})





def redirect_to_long_url(request: 'HttpRequest', short_endpoint: str) -> JsonResponse:
    try:
        url_entry = Url.objects.get(short_endpoint=short_endpoint)

        if url_entry.expiration_date < timezone.now():
            return JsonResponse(data={'error': 'Short URL has expired'}, status=404)
        # I thought about using the ip address and user agent to track the number of redirects and the "user"
        # although this is not a user system, it was designed with that in mind

        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '<unknown>')
        try:
            redirect_entry = Redirect.objects.get(url=url_entry.id)
        except Redirect.DoesNotExist:
            redirect_entry = None

        if redirect_entry:
            redirect_entry.redirect_count += 1
            redirect_entry.save()
        else:
            Redirect.objects.get_or_create(url=url_entry,
                                           ip_address=ip_address,
                                           user_agent=user_agent,
                                           redirect_count=1
                                           )
        logger.info(f"Redirected to {url_entry.long_url} from {short_endpoint} (IP: {ip_address}, User-Agent: {user_agent})")

        return HttpResponseRedirect(url_entry.long_url, status=302)
    except Url.DoesNotExist:
        return JsonResponse({'error': 'Short URL not found'}, status=404)

