arr = [900, 940]
dep = [910, 1200]

#Sort both the arrays

arr.sort()
dep.sort()

i=1
j=0
n=len(arr)
room_req=1
final_ans=0
while i<n and j<n:
    if arr[i]<dep[j]:
        room_req+=1
        i+=1
        if room_req>final_ans:
            final_ans=room_req
    else:
        j+=1
        room_req-=1

print(final_ans)