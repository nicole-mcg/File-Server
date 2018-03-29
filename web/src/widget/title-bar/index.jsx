import React from 'react';

import Button from '../button';
import {Menu} from '../menu'

import './index.less'

import { Link } from 'react-router-dom'
import {cls} from "../../util/"

export default class TitleBar extends React.Component {

  displayName: "TitleBar";

  static get LINKS() {
    return [
      ["Home", ""],
      ["Software", "",
        [
            new Menu.Item("test1", "", function() {}),
            new Menu.Item("test2", "", function() {}),
            new Menu.Item("test3", "", function() {})
        ]
      ],
      ["Blog", "/blog"],
      ["Downloads", "",
        [
            new Menu.Item("test1", "", function() {}),
            new Menu.Item("test2", "", function() {}),
            new Menu.Item("test3", "", function() {})
        ]
      ],
      ["About", "/about"]
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

    var buttons = [];
    for (var i = 0; i < TitleBar.LINKS.length; i++) {
        var selected = selectedIndex === i;
        buttons.push((
            <Menu
              key={i - TitleBar.LINKS.length}
              className={cls(this, "menu")}
              selectedIndex={selected ? selectedSubmenu : []}
              items={TitleBar.LINKS[i][2]}>
              <Link to={TitleBar.LINKS[i][1]}>
                <Button
                  selected={selected}
                  className={cls(this, "button")}>
                    {TitleBar.LINKS[i][0]}
                </Button>
              </Link>
            </Menu>
        ))
    }
    return (
        <div>
          <div className={cls(this)}>
            <div ref="title" className={cls(this, "title")}>Outstream Software</div>
            <div ref="bar" className={cls(this, "bar")}>
                {buttons}
            </div>
          </div>
        </div>
    );
  }
}