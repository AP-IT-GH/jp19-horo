using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Marker2control : MonoBehaviour {

    // Use this for initialization
    void OnEnable()
    {
        WorldCursor.OnTabSetup2 += Teleport;
        WorldCursor.ResetWorld += Reset;
        this.GetComponent<Renderer>().enabled = false;//subscribe op het event
    }


    void OnDisable()
    {
        WorldCursor.OnTabSetup2 -= Teleport;
        WorldCursor.ResetWorld -= Reset;//unsubscribe op het event
    }


    void Teleport(Vector3 pos)
    {
        pos.y += (float)0.074;


        this.transform.position = pos;
        this.GetComponent<Renderer>().enabled = true;

    }
    void Reset()
    {
        this.GetComponent<Renderer>().enabled = false;
    }
}
