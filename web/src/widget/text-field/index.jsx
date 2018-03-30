import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class TextField extends React.Component {
    displayName: "Textfield";

    constructor(props) {
        super(props);
        this.state = {
            value: props.value,
        };
    }

    onChange(event) {
        this.setState({value: event.target.value});
    }

    render() {
        return (
            <div>
                <label style={this.props.style}
                    className={cls(this, "", {
                        selected: this.props.selected
                    }) + " " + this.props.className}>
                    {this.props.name}
                </label>
                <input 
                    value={this.state.value}
                    className={cls(this, "default")}
                    type={this.props.password ? "password" : "text"}
                    onChange={this.onChange.bind(this)}>
                </input>
            </div>
        );
    }
}
TextField.propTypes = {
    className: PropTypes.string,
    name: PropTypes.string,
    value: PropTypes.string,
    password: PropTypes.bool,
};
TextField.defaultProps = {
    className: "",
    name: "",
    value: "",
    password: false,
}