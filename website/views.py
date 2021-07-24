from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User, Community, Usercommunity, Post
from . import db

view = Blueprint('view', __name__)

@view.route('/')
def landing():
    return render_template('index.html')

@view.route('/home')
@login_required
def home():
    return render_template('home.html')

@view.route('/search_communitiez', methods=["POST", "GET"])
@login_required
def search_communitiez():
    """ This function creates the route for the
    user to search for different Communitiez. 
    """
    
    communitiez_list = []
    communities = Community.query.all()

    if request.method == 'POST':
        users_search = request.form['searchCommunitiez'] 
        for x in communities:
            if users_search in x.name:
                community = []
                community.append(x.name)
                community.append(x.category)
                community.append(x.about)
                communitiez_list.append(community)
        
    else: 
        for x in communities:
            community = []
            community.append(x.name)
            community.append(x.category)
            community.append(x.about)
            communitiez_list.append(community)
        
    return render_template('search_communitiez.html', communitiez_list = communitiez_list)

@view.route('search_communitiez/<category>', methods=["POST", "GET"])
@login_required
def search_communitiez_category(category):
    """ This function creates the route for the
    user to search for communtiez via their category. 
    """

    communitiez_list = []
    communities = Community.query.all()

    if request.method == 'POST':
        users_search = request.form['searchCommunitiez'] 
        for x in communities:
            if users_search in x.name:
                community = []
                community.append(x.name)
                community.append(x.category)
                community.append(x.about)
                communitiez_list.append(community)
    
    else: 
        for x in communities:
            if x.category == category or category == 'All':
                community = []
                community.append(x.name)
                community.append(x.category)
                community.append(x.about)
                communitiez_list.append(community)
        
    return render_template('search_communitiez.html', communitiez_list = communitiez_list)
        



@view.route('/create_community', methods=["POST", "GET"])
@login_required
def create_community():
    """ this function creates the route for the user 
    to create a community on Communitiez. It checks 
    to see if the details entered match the criteria
    for Community creation. If the details are sufficient
    the community is created and the details are 
    entered in to the database.  
    """

    if request.method == 'POST':
        community_category = request.form.get('createCommunityDropdown')
        community_name = request.form.get('createCommunityName')
        community_about = request.form.get('createCommunityAbout')

        name_exists = Community.query.filter_by(name=community_name).first()
 
        if name_exists: 
            flash("This community name already exists! Sorry. Try again.", category='error')
        elif len(community_name) < 1:
            flash("Unsufficient amount of characters for the name. Try again.", category='error')
        elif len(community_name) > 200:
            flash("Too many characters in the name. Try again.", category='error') 
        elif len(community_about) < 1:
            flash("Unsufficient amount of characters for the about section. Try again.", category='error')
        elif len(community_about) > 1000:
            flash("Too many characters in the about section. Try again.", category='error') 
        else: 
            new_community = Community(name=community_name, category=community_category, about = community_about)
            db.session.add(new_community)
            db.session.commit()
            flash("Community Created!", category='success')
            return redirect(url_for("view.home"))
        
        return redirect(url_for("view.create_community"))
        
    else: 
        return render_template("create_community.html")

@view.route('/community_page/<community_name>', methods=["POST", "GET"])
@login_required
def community_page(community_name):
    
    is_member = False
    community_details = Community.query.filter_by(name=community_name).first()
    user_community_details = Usercommunity.query.filter_by(user_id=current_user.id, community_id=community_details.id).first()
    if user_community_details is not None:
            is_member = True

    if request.method == 'POST':
        if request.form["hiddenCommunityPageForm"] == "postMessage":
            message = request.form["communityPagePostMessage"]
            heading = request.form["communityPagePostMessageHeading"]
            new_community_post = Post(user_id=current_user.id, community_id=community_details.id, text=message, heading=heading)
            db.session.add(new_community_post)
            db.session.commit()
        else:
            if is_member: 
                db.session.delete(user_community_details)
                db.session.commit()
            else: 
                new_user_community = Usercommunity(user_id=current_user.id, community_id=community_details.id)
                db.session.add(new_user_community)
                db.session.commit()
        return redirect(url_for("view.community_page", community_name=community_name))
    else:  
        community_about = community_details.about
        community_category = community_details.category

        community_post_details = Post.query.filter_by(community_id=community_details.id)
        community_posts = []
        for post in community_post_details:
            community_post = {
                "heading":post.heading, 
                "text":post.text, 
                "date":post.date, 
                "user_id":post.user_id
            }
            community_posts.append(community_post)

        print(community_posts)

        return render_template("community_page.html", community_name=community_name, community_about=community_about, community_category=community_category, is_member=is_member, community_posts=community_posts)