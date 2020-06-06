from django.shortcuts import render
from .stuff import *
from .forms import Add_item, Full_item, Use_item, Search_item




def home(request):
    """Function for the home/startpage with a call for a search function when infromation is submited in the form

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    today = date.today()
    three = today + timedelta(days=3)
    five = today + timedelta(days=5)
    expire = Item.webcheck()
    ingredient = Item.get()
        
    if request.method == 'POST':
        form = Search_item(request.POST)
        if form.is_valid():
            ingredient2 = form.cleaned_data['name']
            search = Item.search(ingredient2)
            form = Search_item()
            freezer = search[0]
            dry = search[1]
            fridge = search[2]
            context = {
                'today': today,
                'three': three,
                'five': five,
                'freezer': freezer,
                'dry': dry,
                'fridge': fridge,
                'form': form,
                'ingredient2': ingredient2,
                'ingredient':ingredient,
                'expire': expire,
            }
            return render(request, 'index/home.html', context)    
    else:
        form = Search_item()
        context = {
        'expire': expire,
        'ingredient':ingredient,
        'today': today,
        'three': three,
        'five': five,
        'form': form,
    }

    return render(request, 'index/home.html', context)

def storage(request):
    """Function for showing the storage webpage with no items

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    context = {
        'title': 'Storage'
        }

    return render(request, 'index/storage.html', context)

def freezerstorage(request):
    """Function for showing the storage webpage with items from the freezer

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    data = Freezer_store.get()
    ingredient = Item.get()
    context = {
        'title': 'Freezer',
        'food': data,
        'ingredient':ingredient

        }

    return render(request, 'index/storage.html', context)

def fridgestorage(request):
    """Function for showing the storage webpage with items from the fridge

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    data = Fridge_store.get()
    ingredient = Item.get()
    context = {
        'title': 'Fridge',
        'food': data,
        'ingredient':ingredient

        }

    return render(request, 'index/storage.html', context)

def drystorage(request):
    """Function for showing the storage webpage with items from the dry storage

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    data = Dry_store.get()
    ingredient = Item.get()
    context = {
        'title': 'Dry',
        'food': data,
        'ingredient':ingredient

        }

    return render(request, 'index/storage.html', context)

def add(request):
    """Function for showing the add page for adding new items
    Usess function calls to check if there is items stored or a new type when information is submted in the form

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    if request.method == 'POST':
        form = Full_item(request.POST)
        if form.is_valid():
            EAN = form.cleaned_data['EAN']
            expiredate = form.cleaned_data['expiredate']
            store = form.cleaned_data['storage']
            amount = form.cleaned_data['amount']
            ingredient = form.cleaned_data['name']
            Item.new_store(ingredient, amount, EAN)
            check = Item.store(store, EAN, expiredate)
            form = Add_item()
            ingredient = Item.get_EAN(EAN)
            context = {
                'check': check,
                'ingredient': ingredient,
                'form' : form,
                'title': 'Add'
            }

            return render(request, 'index/add.html', context)
          
        else:
            form = Add_item(request.POST)
            if form.is_valid():
                EAN = form.cleaned_data['EAN']
                expiredate = form.cleaned_data['expiredate']
                store = form.cleaned_data['storage']
                check = Item.store(store, EAN, expiredate)
                if check == 'no_item':
                    form = Full_item(request.POST)
                    context = {
                            'new': 'Item not in database, please fill the rest',
                            'form': form,
                            'title': 'New item'
                            }
                    return render(request, 'index/add.html', context)
                else:
                    ingredient = Item.get_EAN(EAN)
                    form = Add_item()
                    context = {
                        'form' : form,
                        'title': 'Add',
                        'check': check,
                        'ingredient': ingredient
                        }
                    return render(request, 'index/add.html', context)  
    else:
        form = Add_item()
        context = {
            'form' : form,
            'title': 'Add'
            }

        return render(request, 'index/add.html', context)


def use(request):
    """Function for showing the use page.
    The function calls the use function when information is submitted in the form

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    if request.method == 'POST':
        form = Use_item(request.POST)
        if form.is_valid():
            EAN = form.cleaned_data['EAN']
            amount = form.cleaned_data['amount']
            storage = form.cleaned_data['storage']
            stored = Item.use(EAN, amount, storage)
            form = Use_item()
            if stored[0] == 'to-much':
            
                context = {
                    'item': Item.get_EAN(EAN),
                    'amount': amount,
                    'tomuch': stored[1],
                    'form': form,
                    'title': 'Use'
                }
                return render(request, 'index/use.html', context)
            else:
                context = {
                    'item': Item.get_EAN(EAN),
                    'amount': amount,
                    'ok': stored[1] - amount,
                    'form': form,
                    'title': 'Use'
                }
                return render(request, 'index/use.html', context)
 
    form = Use_item()
    context = {
            'form': form,
            'title': 'Use'
        }
    return render(request, 'index/use.html', context)


def delete(request):
    """Function for displaying the delete page for manual deletion.
    Uses the same search functionm as the home/start page

    Arguments:
        request {django} -- django

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    today = date.today()
    three = today + timedelta(days=3)
    five = today + timedelta(days=5)
    ingredient = Item.get()
        
    if request.method == 'POST':
        form = Search_item(request.POST)
        if form.is_valid():
            ingredient2 = form.cleaned_data['name']
            search = Item.search(ingredient2)
            form = Search_item()
            freezer = search[0]
            dry = search[1]
            fridge = search[2]
            context = {
                'today': today,
                'three': three,
                'five': five,
                'freezer': freezer,
                'dry': dry,
                'fridge': fridge,
                'form': form,
                'ingredient':ingredient,
            }
            return render(request, 'index/delete.html', context)    
    else:
        form = Search_item()
        context = {
        'form': form,
    }

    return render(request, 'index/delete.html', context)


def delete_confirmation(request, storage, id):
    """Function for displaying the delete confirmation page

    Arguments:
        request {django} -- django
        storage {string} -- tells the systen from which storage you are planning to delete an item
        id {integer} -- tells the system which item id you are about to delete

    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """

    item = Item.del_conf(storage, id)
    ingredient = Item.get()
    context = {
     'item': item,
    'ingredient':ingredient,
    'storage': storage,
     'confirm': 'confirm'
    }
    return render(request, 'index/delete.html', context)

def deteled(request, confirmed, storage, id):

    """Function for showing the item deleted

    Arguments:
        request {django} -- django
        storage {string} -- tells the systen from which storage you are planning to delete an item
        id {integer} -- tells the system which item id you are about to delete
        confirmed {string} -- placeholder for telling the system to go ahead and delete


    Returns:
        Render -- Returns a render to the HTML page corresponding with information needed
    """
    

    item = Item.del_conf(storage, id)
    ingredient = Item.get()
    Item.delete(storage, id)
    context = {
    'item': item,
    'ingredient':ingredient,
    'storage': storage,
    'reload': 'reload',
    }
    return render(request, 'index/delete.html', context)