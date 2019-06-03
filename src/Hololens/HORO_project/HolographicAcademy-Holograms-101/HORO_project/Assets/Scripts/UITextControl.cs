using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UITextControl : MonoBehaviour {

    // Use this for initialization
    void OnEnable()
    {
        WorldCursor.OnClicked += Teleport;
        WorldCursor.ResetWorld += Reset;
        this.GetComponent<Renderer>().enabled = false;//subscribe op het event
    }


    void OnDisable()
    {
        WorldCursor.OnClicked -= Teleport; //unsubscribe op het event
        WorldCursor.ResetWorld -= Reset;
    }


    void Teleport(Vector3 pos)
    {


        pos.y += (float)0.21;
        pos.x -= (float)0.13;
        this.GetComponent<TextMesh>().text = "Location of detected object is "+pos;
        this.transform.position = pos;
        this.GetComponent<Renderer>().enabled = true;

    }
    void Reset()
    {
        this.GetComponent<Renderer>().enabled = false;
    }
}
