from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class HomeView(View):
  def get(self, *args, **kwargs):
    context = {}
    return render(self.request, 'base/index.html', context)


class ChargeView(View):
  def post(self, *args, **kwargs):
    amount = int(self.request.POST.get('amount'))
    token = self.request.POST.get('stripeToken')
    email = self.request.POST.get('email')
    name = self.request.POST.get('nickname')

    try:
      customer = stripe.Customer.create(
        email= email,
        name=name,
        source = token,
        description = 'A donor'
      )

      stripe.Charge.create(
        customer=customer,
        amount = amount * 100,
        currency = "usd",
        description= "Donation"
      )

      return redirect('base:success', args=amount)

    except stripe.error.CardError as e:
      print('Status is: %s' % e.http_status)
      print('Type is: %s' % e.error.type)
      print('Code is: %s' % e.error.code)
      # param is '' in this case
      print('Param is: %s' % e.error.param)
      print('Message is: %s' % e.error.message)
      messages.warning(self.request, f'{e.error.message}')
      return redirect('base:index')
    except stripe.error.RateLimitError as e:
      messages.warning(self.request, 'RateLimit Error')
      return redirect('base:index')
    except stripe.error.InvalidRequestError as e:
      messages.warning(self.request, 'InvalidRequest Error')
      return redirect('base:index')
    except stripe.error.AuthenticationError as e:
      messages.warning(self.request, 'Authentication Error')
      return redirect('base:index')
    except stripe.error.APIConnectionError as e:
      messages.warning(self.request, 'Network Error')
      return redirect('base:index')
    except stripe.error.StripeError as e:
      messages.warning(self.request, 'Something went wrong. You were not charged. Please try again')
      return redirect('base:index')
    except Exception as e:
      messages.warning(self.request, 'A server error occurred. We have been notified')
      return redirect('base:index')


def success_msg(request, args):
  amount = args
  context = {'amount': args}
  return render(request, 'base/success.html', context)