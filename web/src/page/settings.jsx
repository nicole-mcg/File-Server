import React from "react";

import ContentSpacer from "../widget/content-spacer";
import CheckBox from "../widget/check-box"
import RadioButton from "../widget/radio-button";
import AddButton from "../widget/add-button";
import InfoPane from '../widget/info-pane';
import SubTitle from '../widget/sub-title';

import Img from 'react-image'

import {cls, constants} from "../util/"

export default class SettingsPage extends React.Component {
    render() {

        return (
            <div>
                <InfoPane title="Profile Settings" size="large">

                    <SubTitle>subtitle:</SubTitle>
                    <ContentSpacer>
                        <RadioButton value="radio" group="gender">radio</RadioButton>
                        <RadioButton value="buttons" group="gender">buttons</RadioButton>
                        <CheckBox value="checkbox">checkbox</CheckBox>
                        <AddButton>Add another</AddButton>
                    </ContentSpacer>
                    
                </InfoPane>
            </div>
        );
    }
};