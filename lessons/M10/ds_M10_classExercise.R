#Exercise 1
F<-numeric(10) #initialize a vector of length 10 
F[1]<-F[2]<-1
for (i in 3:10){
  F[i]<-F[i-2]+F[i-1]
}
print(F)

#Exercise 2
get<-function(n=10){
  F<-numeric(n)
  F[1]<-F[2]<-1
  for (i in 3:n){
    F[i]<-F[i-2]+F[i-1]
  }
  return(F)
}

#Exercise 3
get2<-function(x){
  if (x<=1 & x>=1){
    return(1)
  } else {
    return(0)
  }
}

#Exercise 4
get2(1)
get2(0)
get2(-1)
get2(4)
get2(5)

#Exercise 5
head(letters[1:10])
head(letters, 10)

tail(LETTERS, 10)
L=length(LETTERS);L
print(LETTERS[(L-9):L])

#Exercise 6
for (n in 1:100){
  if (n %%3 == 0 && n %% 5 == 0){
    print(paste(n,"FixxBuzz"))
  }
else if (n %% 3 == 0) {
  print(paste(n,"Fizz"))
}
else if (n %% 5 == 0)
  print(paste(n,"Fixx"))
}
  print(n)

