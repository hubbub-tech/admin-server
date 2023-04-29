from datetime import datetime

from src.models import Items
from src.models import Users

from src.utils.settings import smtp_config

from ._email_body import EmailBodyMessenger, EmailBodyFormatter


def get_sunset_email(user):

    email_body_messenger = EmailBodyMessenger()
    email_body_formatter = EmailBodyFormatter()

    # user = Users.get({"id": order.renter_id})

    """
    You can keep your item(s). This means you can take them with you to your summer housing or back home or store them. With this option, Hubbub would just keep the initial deposit on your item(s), and then they’re all yours–for a fraction of the price!
    You can donate your item(s). With the majority of our users being either NYU or Columbia students, we’ve made it easy for you to do this by providing details on how to do this on either campus. For Columbia, fill out this form or look out for more information on the donation program Give and Go Green here. For NYU, click here for tips and look out for more potential updates here. With this option, Hubbub would keep the initial deposit on your item(s).
    You can sell your item(s). There are many ways and platforms for selling that you can post your item(s) on to make some $$$. Some key resources we'd recommend would include (1) Facebook Marketplace, (2) OfferUp (app), (3) Columbia/NYU buy/sell Facebook pages. With this option, Hubbub would keep the initial deposit on your item(s).

    If none of these options sound like they’d work for your circumstances, you can reach out to us at hello@hubbub.shop to see if there’s anything else we can figure out together. 

    Things are different this time around as we’ve decided to put Hubbub’s current operations on pause. Our team is figuring out what the next evolution of Hubbub might look like but in the meantime we appreciate your patience!
    """

    email_body_formatter.preview = f"An important update to Hubbub operations over the next few months"

    email_body_formatter.user = user.name

    email_body_formatter.introduction = """
        First off, we the co-founders and operators of Hubbub – Ade, Caro, and Patrick – would like to thank every one 
        of you for your continued support and acceptance of this new way of getting what you need for only as long as 
        you need it. We wouldn’t have made it this far without your belief in us.
        """

    email_body_formatter.content = """
        Looking ahead to the upcoming months, we know that most of you have item rentals that end in April/May or beyond. 
        We wanted to reach out with some anticipation to let you all know that things are going to be a bit different this year. 
        <strong> Most importantly, we won’t be reaching out to coordinate individual pick-ups like we normally do. </strong>
        Instead, we are providing you with the following options:
        </p>
        <ol>
            <li>
                <strong>You can keep your item(s).</strong> This means you can take them with you to your summer housing or 
                back home or store them. With this option, Hubbub would just keep the initial deposit on your item(s), and 
                then they’re all yours.
            </li>
            <li>
                <strong>You can donate your item(s).</strong> With the majority of our users being either NYU or Columbia students, 
                we’ve made it easy for you to do this by providing details on how to do this on either campus. For Columbia, fill out this 
                <a href='https://docs.google.com/forms/d/e/1FAIpQLSeQT4TKVSpAfvyZ2l8tUqXX5JHd_t4B7DZg4xtf6iMhrbOUhA/viewform'>form</a> 
                or look out for more information on the donation program Give and Go Green <a href='https://www.instagram.com/columbia.ecoreps/?hl=en'>here</a>. 
                For NYU, click <a href='https://wp.nyu.edu/sustainability-nyusustainablog/2021/05/03/reduce-waste-and-donate-resources-for-a-sustainable-move-out/'>here</a> 
                for tips and look out for more potential updates <a href='https://www.instagram.com/nyu_green/'>here</a>. With this option, Hubbub 
                would keep the initial deposit on your item(s).
            </li>
            <li>
                <strong>You can sell your item(s).</strong> There are many ways and platforms for selling that you can post your 
                item(s) on to make some $$$. Some key resources we'd recommend would include (1) Facebook Marketplace, (2) OfferUp (app), 
                (3) Columbia/NYU buy/sell Facebook pages. With this option, Hubbub would keep the initial deposit on your item(s).
            </li>
        </ol>
        <p>
            If none of these options sound like they’d work for your circumstances, you can reach out to us at hello@hubbub.shop to 
            see if there’s anything else we can figure out together.
        """

    email_body_formatter.conclusion = f"""
        Things are different this time around as we’ve decided to put Hubbub’s current operations on pause. Our team is figuring 
        out what the next evolution of Hubbub might look like but in the meantime we appreciate your patience!
        """

    body = email_body_formatter.build()

    email_body_messenger.subject = "[Hubbub] On Spring 2023 Operations"
    email_body_messenger.to = (user.email, smtp_config.DEFAULT_RECEIVER)
    email_body_messenger.body = body
    return email_body_messenger
