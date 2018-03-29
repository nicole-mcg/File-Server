import React from 'react';

import './index.less'

import { Link } from 'react-router-dom'

import {cls} from "../../util/"

class MenuItem {
    constructor(text, link, callback=function() {}) {
        this.text = text;
        this.link = link;
        this.callback = callback;
    }
}

export class Menu extends React.Component {
    displayName: "Menu";

    render() {

        var selectedIndex = this.props.selectedIndex.slice(0).shift()

        var menuItems = this.props.items;

        var menuComponents = []
        if (menuItems != null) {
            for (var i = 0; i < menuItems.length; i++) {
                menuComponents.push(
                    <Link to={menuItems[i].link} key={i}>
                        <div key={i} className={cls(this, "item", {selected: selectedIndex == i})}>
                            {menuItems[i].text}
                        </div>
                    </Link>
                );
            }
        }

        //TODO submenus!!
        var children = (
            <div className={cls(this, "container")}>
                {this.props.children}
                <div className={cls(this, "menu") + " " + this.props.className}>
                    {menuComponents}
                </div>
            </div>
        );

        return children;
    }
}

exports.Menu.Item = MenuItem;