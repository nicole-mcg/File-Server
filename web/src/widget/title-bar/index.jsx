import React from 'react';
import PropTypes from 'prop-types';

import Button from '../button';
import {Menu} from '../menu';

import './index.less';

import { Link } from 'react-router-dom';
import {cls} from "../../util/";

export default class TitleBar extends React.Component {

  displayName: "TitleBar";

  get_links() {
    var name = "N/A";
    if (this.props.user) {
      name = this.props.user.name;
    }
    return [
      ["Home", ""],
      ["Files", "/files"],
      ["###", "",
        [
            new Menu.Item("test1", "", function() {}),
            new Menu.Item("test2", "", function() {}),
            new Menu.Item("test3", "", function() {})
        ]
      ],
      ["Settings", "/settings"],
      [name, "",
          [
              new Menu.Item("Logout", "/logout", function() {}),
          ]
      ]
    ];
  }

  constructor() {
    super();
    this.handleScroll = this.handleScroll.bind(this)
  }

  componentDidMount() {
      window.addEventListener('scroll', this.handleScroll);
  }

  componentWillUnmount() {
      window.removeEventListener('scroll', this.handleScroll);
  }

  handleScroll(event) {
    var scrollTop = event.srcElement.body.scrollTop;
    var title = this.refs.title;
    var bar = this.refs.bar;


    var yPos = title.getBoundingClientRect().top + title.clientHeight;
    bar.style.position = scrollTop > yPos ? "fixed" : "static";
  }

  render() {

    var selectedIndex = this.props.selectedIndex.slice(0).shift();//TODO make this accept single values
    var selectedSubmenu = this.props.selectedIndex.slice(0);

    var links = this.get_links();

    var buttons = [];
    for (var i = 0; i < links.length; i++) {
        var selected = selectedIndex === i;
        buttons.push((
            <Menu
              key={i - links.length}
              className={cls(this, "menu")}
              selectedIndex={selected ? selectedSubmenu : []}
              items={links[i][2]}
              fit_content
              link>
              <Link to={links[i][1]}>
                <Button
                  selected={selected}
                  className={cls(this, "button")}
                  nav>
                    {links[i][0]}
                </Button>
              </Link>
            </Menu>
        ))
    }
    return (
        <div>
          <div className={cls(this)}>
            <div ref="title" className={cls(this, "title")}>File Server</div>
            <div ref="bar" className={cls(this, "bar")}>
                {buttons}
            </div>
          </div>
        </div>
    );
  }
}

TitleBar.propTypes = {
  selectedIndex: PropTypes.array,
  user: PropTypes.object
}
TitleBar.defaultProps = {
  selectedIndex: [],
  user: {}
}