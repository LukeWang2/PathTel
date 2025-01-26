import React from 'react';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import leacockImage from '../floorplans/leacock.jpeg';

const InteractiveFloorPlan = () => {
    return (
        <TransformWrapper>
            <TransformComponent>
                <img 
                    src={leacockImage} 
                    alt="Interactive Floor Plan" 
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'contain',
                    }}
                />
            </TransformComponent>
        </TransformWrapper>
    );
};

export default InteractiveFloorPlan;