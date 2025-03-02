# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Team

def register_team(request):
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_leader = request.POST['team_leader']
        team_leader_email = request.POST['team_leader_email']
        members_count = int(request.POST['members_count'])
        member_emails = request.POST['member_emails']
        password = request.POST['password']

        if members_count > 4:
            messages.error(request, "A team can have at most 4 members.")
            return render(request, 'register.html')

        # Ensure team leader email is included in the members list
        emails = set(member_emails.split(',')) | {team_leader_email}
        all_member_emails = ','.join(emails)

        if Team.objects.filter(team_name=team_name).exists():
            messages.error(request, "Team name already taken.")
            return render(request, 'register.html')

        if Team.objects.filter(team_leader_email=team_leader_email).exists():
            messages.error(request, "Team leader email already registered.")
            return render(request, 'register.html')

        team = Team(
            team_name=team_name,
            team_leader=team_leader,
            team_leader_email=team_leader_email,
            members_count=members_count,
            member_emails=all_member_emails
        )
        team.set_password(password)
        team.save()

        messages.success(request, "Team registered successfully! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_team(request):
    if request.method == 'POST':
        team_name = request.POST['team_name']
        password = request.POST['password']
        try:
            team = Team.objects.get(team_name=team_name)
            if team.check_password(password):
                request.session['team_name'] = team_name  # Store session
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
        except Team.DoesNotExist:
            messages.error(request, "Invalid team name.")

    return render(request, 'login.html')


def logout_team(request):
    request.session.flush()
    return redirect('login')
