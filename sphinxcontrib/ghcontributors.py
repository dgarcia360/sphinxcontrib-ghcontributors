# -*- coding: utf-8 -*-

import requests
from docutils import nodes
from docutils.parsers.rst import directives, Directive
import logging

logger = logging.getLogger(__name__)


def _render_contributor(contributor):

    # name and url
    node_paragraph = nodes.paragraph()
    node_url = nodes.reference(text=contributor.get('login'), refuri=contributor.get('html_url'))
    node_paragraph += node_url

    # number of contributions
    contributions = contributor.get('contributions')
    node_contributions = nodes.Text(' - ' + str(contributions) + ' ' +
                                    ('contributions' if contributions != 1 else 'contribution'))
    node_paragraph += node_contributions

    return node_paragraph


def _render_contributors_list(contributors):

    contributors = sorted(contributors, key=lambda k: k['contributions'], reverse=True)

    lst = nodes.bullet_list()

    for c in contributors:
        list_item = nodes.list_item()
        list_item += _render_contributor(c)
        lst += list_item

    return lst


def _get_gh_contributors(owner, repository):

    contributors = []

    try:
        r = requests.get('https://api.github.com/repos/' + owner + '/' + repository + '/contributors')
        if r:
            contributors = r.json()

    except Exception as e:
        logger.error(e)

    return contributors


class ContributorsDirective(Directive):

    has_content = True

    option_spec = {
        'owner': directives.unchanged,
        'repository': directives.unchanged
    }

    def run(self):

        owner = self.options.get('owner')
        repository = self.options.get('repository')

        contributors = _get_gh_contributors(owner, repository)

        return [_render_contributors_list(contributors)]


def setup(app):

    app.add_directive('ghcontributors', ContributorsDirective)