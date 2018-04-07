import React from 'react';
import PropTypes from 'prop-types';

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
                var element = (
                    <div key={i} className={cls(this, "item", {selected: selectedIndex == i})} onClick={menuItems[i].callback}>
                        {menuItems[i].text}
                    </div>
                )
                if (this.props.link) {
                    menuComponents.push(
                        <Link to={menuItems[i].link} key={i}>
                            {element}
                        </Link>
                    );
                } else {
                    menuComponents.push(element);
                }
            }
        }


        //TODO submenus!!
        var children = (
            <div className={cls(this, "container", {fitContent: this.props.fit_content})} onMouseLeave={this.props.onMouseLeave}>
                {this.props.children}
                <div className={cls(this, "menu") + " " + this.props.className} >
                    {menuComponents}
                </div>
            </div>
        );

        return children;
    }
}
Menu.propTypes = {
    className: PropTypes.string,
    fit_content: PropTypes.bool,
    items: PropTypes.arrayOf(PropTypes.instanceOf(MenuItem)),
    link: PropTypes.bool,
    onMouseLeave: PropTypes.func,
    selectedIndex: PropTypes.arrayOf(PropTypes.number)
}
Menu.defaultProps = {
    className: "",
    fit_content: false,
    items: [],
    link: false,
    onMouseLeave: (e) => {},
    selectedIndex: []
}

exports.Menu.Item = MenuItem;
